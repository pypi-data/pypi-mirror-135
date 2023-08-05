"""
cdf_helpers.py

High level functionality built on top of Cognite's Python SDK

Most functions require the global cdf client to be set up before using them.
"""
import time
import sys
import os 
import json
import functools
from datetime import datetime
from shutil import make_archive, unpack_archive
from multiprocessing import Pool
from functools import partial


from cognite.client.exceptions import CogniteNotFoundError, CogniteAPIError
from cognite.client.data_classes import FileMetadataUpdate

from akerbp.mlops.core import config, logger
from akerbp.mlops.core.helpers import confirm_prompt

logging=logger.get_logger(name='mlops_cdf')

global_client = {}
api_keys=config.api_keys

env_vars = {k.upper():str(v) for k,v in config.envs_dic.items() if v}
env_vars.update({'PLATFORM':'cdf'})
try:
    env_vars.pop('GOOGLE_PROJECT_ID')
except KeyError:
    pass


def set_up_cdf_client(context='run'):
    """
    Set up the global client used by most helpers. This needs to be called
    before using any helper. 

    Input:
      - context: string either 'run' (access to data and functions) or 'deploy'
        (access to 'functions' also).
    """
    if context == 'run':
        api_key_labels=["data", "files"]
    elif context == 'deploy':
        api_key_labels=["data", "files", "functions"]
    else:
        raise ValueError("Context should be either 'run' or 'deploy'")

    for k in api_key_labels:
        if k not in global_client:
            global_client[k] = get_client(api_keys[k], k)
        
    logging.debug("CDF client was set up correctly")


def get_client(api_key, api_key_label=None):
    """
    Create a CDF client with a given api key
    """
    if not api_key:
        raise ValueError("CDF api key is missing")
    
    if api_key_label == 'functions':
        from cognite.experimental import CogniteClient
        logging.warning("Imported CogniteClient from cognite.experimental")
    else:
        from cognite.client import CogniteClient
    
    client = CogniteClient(
        api_key=api_key,
        project='akbp-subsurface',
        client_name="mlops-client",
        base_url='https://api.cognitedata.com'
    )
    assert client.login.status().logged_in
    logging.debug(f"{client.version=}")
    return client


def validate_function_name(function_name, verbose=True):
    """
    Validate that function name follows MLOps standard: model-service-env

    Input: (string) function name to validate
    Output: (bool) True if name is valid, False otherwise
    """
    supported_services = ["prediction", "training"]
    supported_environments = ["dev", "test", "prod"]
    try:
        model, service, environment = function_name.split("-")
    except ValueError:
        if verbose:
            m = f"Expected function name format: 'model-service-environment'"
            logging.error(m)
        return False
    if service not in supported_services:
        if verbose:
            m = f"Supported services: {supported_services}"
            logging.error(m)
        return False
    if environment not in supported_environments:
        if verbose:
            m = f"Supported environments: {supported_environments}"
            logging.error(m)
        return False
    return True


def delete_function(function_name, confirm=True):
    """
    Delete a deployed function 

    Input:
        - function_name: (string) function name (external id), with the format
            'model_name-service-environment'. Use `list_functions` to get an
            overview of deployed functions
        - confirm: (bool) whether the user will be asked to confirm deletion
    """
    if not validate_function_name(function_name):
        raise ValueError()
    model, service, environment = function_name.split("-")

    confirmed = False

    if confirm:
        question = f"Delete {model=}, {service=}, {environment=}?"
        confirmed = confirm_prompt(question)

    if not confirm or confirmed:
        client = global_client["functions"]
        try:
            client.functions.delete(external_id=function_name)
            logging.debug(f"Deleted function with {function_name=}")
        except CogniteNotFoundError:
            logging.error(f"Couldn't find function with '{function_name=}'")


def create_function_from_folder(
    function_name, 
    folder, 
    handler_path,  
    description='',
    owner='',
    secrets={}
):
    """
    Create a Cognite function from a folder. Any existing function with the same
    name is deleted first.

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - description: (string) function documentation
      - owner: (string) the function's owner's email
      - secrets: api keys or similar that should be passed to the function
    """
    client = global_client["functions"]
    try:
        client.functions.delete(external_id=function_name)
        logging.debug(f"Deleted function {function_name}")
    except CogniteNotFoundError:
        pass
    
    function = client.functions.create( 
        name=function_name, 
        folder=folder, 
        function_path=handler_path,
        external_id=function_name,
        description=description,
        owner=owner,
        secrets=secrets,
        env_vars=env_vars
    )
    logging.debug(
        f"Created {function_name}: {folder=}, {handler_path=}, {env_vars=}"
    )

    return function


def create_function_from_file(
    function_name, 
    file_id, 
    description,
    owner,
    secrets={}
):
    """
    Create a Cognite function from a file deployed to CDF Files. CDF raises
    exception if there's an existing function with the same name.

    Inputs:
      - function_name: (string) name of the function to create
      - file_id: (int) the id for the function file in CDF Files
      - description: (string) function documentation
      - owner: (string) the function's owner's email
      - secrets: (optional) api keys or similar that should be passed to the
        function
    """
    client = global_client["functions"]
    
    function = client.functions.create( 
        name=function_name, 
        file_id=file_id,
        external_id=function_name,
        description=description,
        owner=owner,
        secrets=secrets,
        env_vars=env_vars
    )
    logging.debug(
        f"Created {function_name}: {file_id=}, {env_vars=}"
    )

    return function


def robust_create(create_function):
    """
    Robust creation of a CDF Function. Wait until the function status is ready
    or failed. If it fails, it will try again `max_error` times

    Inputs:
      - create_function: function that creates the CDF function
    """
    max_errors = 3

    for trial in range(max_errors):
        function = create_function()
        status = wait_function_status(function)
        logging.debug(f"Function status is {status}")
        if function.status == 'Ready':
            break
        if function.status == 'Failed' and trial < max_errors-1:
            logging.warning(f"Function failed: {function.id=}")
            logging.debug(f"Error was: {function.error=}")
            logging.debug(f"Try to create function again")
        else:
            raise Exception(f"Function deployment error: {function.error=}")


def deploy_function(
    function_name,
    folder='.',
    handler_path='handler.py',
    secrets=api_keys,
    info={'description':'', 'owner':''}
):
    """
    Deploys a Cognite function from a folder. 

    Inputs:
      - function_name: name of the function to create
      - folder: path where the source code is located
      - handler_path: path to the handler file
      - secrets: api keys or similar that should be passed to the function
    """
    f = functools.partial(
        create_function_from_folder,
        function_name, 
        folder, 
        handler_path, 
        info['description'],
        info['owner'],
        secrets
    )
    robust_create(f)
 

def redeploy_function(
    function_name,
    file_id,
    description,
    owner,
    secrets=api_keys
):
    """
    Deploys a Cognite function from a folder. 

    Inputs:
      - function_name: name of the function to create
      - file_id: (int) the id for the function file in CDF Files
      - owner: (string) the function's owner's email
      - secrets: (optional) api keys or similar that should be passed to the
        function
    """
    f = functools.partial(
        create_function_from_file,
        function_name, 
        file_id, 
        description,
        owner,
        secrets
    )
    robust_create(f)      


def get_function_metadata(function_id):
    """
    Generate metadata for a function
    Input:
        - function_id: (int) function's id in CDF
    Output:
        - (dictionary) function's metadata
    """
    client = global_client["functions"]
    function = client.functions.retrieve(id=function_id)

    ts = function.created_time/1000
    created_time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    metadata = dict(
        external_id=function.external_id,
        description=function.description,
        owner=function.owner,
        status=function.status,
        file_id=function.file_id,
        created_time=created_time
    )
    return metadata


def call_function(function_name, data):
    """
    Call a function deployed in CDF

    Input:
        - function_name: (string) function's external id in CDF
        - data: (dictionary) data for the call
    Output:
        - (dictionary) function's response
    """
    client = global_client["functions"]
    function = client.functions.retrieve(external_id=function_name)
    logging.debug(f"Retrieved function {function_name}")
    call_complete = False
    t_start = time.process_time()
    while not call_complete:
        try:
            call = function.call(data)
            call_complete = True
        except CogniteAPIError:
            logging.warning(f"Cognite API error, try again")
    logging.debug(f"Called function ({call.id=})")
    response = call.get_response()
    t_proc = time.process_time() - t_start
    logging.debug(f"Call complete ({call.id=}, {t_proc=}): {response=}")
    return response


def call_function_process_wrapper(function_name, data):
    """
    Set up the cdf client and call a function. This wrapper makes it possible to call a function from an independent processess invoked by the multiprocessing library
    
    Input:
        - function_name: (string) function's external id in CDF
        - data: (dictionary) data for the call
    Output:
        - (dictionary) function's response
    """
    set_up_cdf_client(context='deploy')
    return call_function(function_name, data)


def call_function_parallel(function_name, data, n_calls=None):
    """
    Make parallel calls to a function deployed in CDF

    Input:
        - function_name: (string) function's external id in CDF
        - data: (list of dictionaries) list of data for the call
        - n_calls: (optional int) number of parallel calls (set None to use all 
            available cpu cores)
    """
    f = partial(call_function_process_wrapper, function_name)
    with Pool(n_calls) as p:
        return p.map(f, data)


def test_function(function_name, data):
    """
    Call a function with data and verify that the response's 
    status is 'ok'
    """
    logging.debug(f"Test function {function_name}")
    if not validate_function_name(function_name):
        raise ValueError()
    output = call_function(function_name, data)
    assert output['status'] == 'ok'
    logging.info(f"Test call was successful :)")


def wait_function_status(function, status=["Ready", "Failed"]):
    """
    Wait until function status is in `status`
    By default it waits for Ready or Failed, which is useful when deploying.
    It implements some control logic, since polling status can fail.
    """
    polling_wait_seconds_base = 10
    polling_wait_seconds = polling_wait_seconds_base
    max_api_errors_base = 5
    max_api_errors = max_api_errors_base
    
    logging.debug(f"Wait for function to be ready or to fail")
    while not (function.status in status):
        try:
            time.sleep(polling_wait_seconds)
            function.update()
            logging.debug(f"{function.status=}")
            polling_wait_seconds = polling_wait_seconds_base
            max_api_errors = max_api_errors_base
        except CogniteAPIError as e:
            max_api_errors -= 1
            logging.warning(f"Could not update function status, will try again")
            polling_wait_seconds *= 1.2          
            if not max_api_errors:
                logging.error(f"Could not update function status.")
                raise e

    return function.status


def list_functions(tags=[], env=None):
    """
    List deployed functions, optionally filtering by environment (dev, test 
    or prod) or set of tags. 
    
    Input:
        - tags: ([string]): list of tags to search for in the function
        description (or-search)
        - env: (string) the environment
    
    Output:
        - ([string]): list of function names (i.e. external_id's )
    """ 
    client = global_client["functions"]
    functions = client.functions.list(limit=-1)
    validate_function = (
        lambda f: validate_function_name(f.external_id, verbose=False)
    )
    functions = filter(validate_function, functions)
    if env:
        get_function_environment = lambda f: f.external_id.split("-")[2]
        env_index = lambda f: get_function_environment(f) == env
        functions = filter(env_index, functions)
    if tags:
        contains_tag = lambda f,t: True if t in f.description else False
        tags_index = lambda f: any([contains_tag(f,t) for t in tags])
        functions = filter(tags_index, functions)
    functions = [f.external_id for f in functions]
    return functions


def download_file(id, path):
    """
    Download file from Cognite
    
    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
        - path: path of local file to write
    """
    client = global_client["files"]
    
    logging.debug(f"Download file with {id=} to {path}")
    client.files.download_to_path(path, **id)


def upload_file(
    external_id, 
    path, 
    metadata={}, 
    directory='/',
    overwrite=True,
    dataset_id=None):
    """
    Upload file to Cognite
    
    Params:
        - external_id: external id
        - path: path of local file to upload
        - metadata: dictionary with file metadata
        - overwrite: what to do when the external_id exists already
        - dataset_id: (int) dataset id
    """
    client = global_client["files"]
    
    metadata = {k:v if isinstance(v, str) else json.dumps(v) 
        for k,v in metadata.items()}

    logging.debug(f"Upload file {path} with {external_id=} and {metadata=}")
    file_info = client.files.upload(
        path, 
        external_id, 
        metadata=metadata, 
        directory=directory, 
        overwrite=overwrite,
        data_set_id=dataset_id
    )
    logging.info(f"Uploaded file: {file_info=}")
    return file_info


def upload_folder(
    external_id, 
    path, 
    metadata={}, 
    overwrite=False, 
    target_folder='/',
    dataset_id=None
):
    """
    Upload folder content to Cognite. It compresses the folder and uploads it.
    
    Params:
        - external_id: external id (should be unique in the CDF project)
        - path: (Path) path of local folder where content is stored
        - metadata: dictionary with file metadata
        - target_folder: path where compressed file should be stored
        - overwrite: if overwrite==False and `external_id` exists => exception
        - dataset_id: (int) dataset id
    """
    base_name = path / 'archive'
    archive_name = make_archive(base_name, 'gztar', path)
    file_info = upload_file(
        external_id, 
        archive_name, 
        metadata=metadata,
        overwrite=overwrite,
        directory=target_folder,
        dataset_id=dataset_id
    )
    os.remove(archive_name)
    logging.info(f"Folder content uploaded: {file_info=}")
    return file_info


def download_folder(external_id, path):
    """
    Download content from Cognite to a folder. It is assumed to have been
    uploaded using `upload_folder()`, so it downloads a file and decompresses
    it.

    Params:
    - external_id: external id
    - path: (Path) path of local folder where content will be stored
    """
    base_name = path / 'archive.tar.gz'
    download_file(dict(external_id=external_id), base_name)
    unpack_archive(base_name, base_name.parent)
    os.remove(base_name)
    logging.info(f"Model file/s downloaded to {path}")


def log_system_info():
    """
    Can be called from a handler to log CDF environment information
    """
    logging.debug(f"Python version:\n{os.popen('python --version').read()}")
    logging.debug(f"Python path:\n{sys.path}")
    logging.debug(f"Current working directory:\n{os.getcwd()}")
    logging.debug(f"Content:\n{os.popen('ls -la *').read()}")
    logging.debug(f"Packages:\n{os.popen('pip freeze').read()}")


def query_file_versions(
    directory_prefix, 
    external_id_prefix, 
    metadata={}, 
    uploaded=True,
    dataset_id=None):
    """
    Find all file versions that match a query. 

    Input:
        -directory_prefix
        -external_id_prefix
        -metadata: query to the metadata (dictionary)
        -uploaded: (bool)
        -dataset_id: (int) dataset id
    Output:
        - list of versions (dataframe)
    """
    client = global_client["files"]
    file_list = client.files.list(
        limit=-1, 
        directory_prefix=directory_prefix, 
        external_id_prefix=external_id_prefix,
        metadata=metadata,
        uploaded=uploaded,
        data_set_ids=dataset_id
    ).to_pandas()

    return file_list


def delete_file(id):
    """
    Delete file from Cognite
    
    Params:
        - id: dictionary with id type (either "id" or "external_id") as key
    """
    client = global_client["files"]
    client.files.delete(**id)
    logging.debug(f"Deleted file with {id=}")


def copy_file(source_ext_id, target_ext_id, overwrite=False, dataset_id=None):
    """
    Copy content and metadata of a file in CDF Files

    Input:
        - source_ext_id: (str) external id for source file
        - target_ext_id: (str) external id for target file
        - overwrite: (bool) should target file be overwritten if it exists
        - dataset_id: (int) dataset id for the target file
    """
    client = global_client["files"]
    f = client.files.retrieve(external_id=source_ext_id)
    file_content = client.files.download_bytes(external_id=source_ext_id)
    logging.debug(f"Downloaded file: {source_ext_id}, {f.dump()}")
    f = client.files.upload_bytes(
        file_content, 
        name=f.name,
        external_id=target_ext_id,
        metadata=f.metadata, 
        directory=f.directory, 
        overwrite=overwrite,
        data_set_id=dataset_id
    )
    m = f"Copied source {source_ext_id} to {target_ext_id}, {f.dump()}"
    logging.info(m)


def file_exists(external_id, directory, dataset_id=None):
    """
    Check if a file exists in a folder (regardless of uploaded status)

    Input:
        - external_id: (str)
        - directory: (str)
        - dataset_id: (int)
    Output
        - exists: (bool)
    """
    file_list = query_file_versions(
        directory_prefix=directory, 
        external_id_prefix=external_id,
        uploaded=None, dataset_id=dataset_id
    )
    if file_list.empty:
        logging.info(f"File with '{external_id=}' not found")
        exists = False
    else:
        exists = True
    return exists


def get_dataset_id(external_id):
    """
    Input:
        -external_id: (str) dataset external id, or `None` for no dataset
    Output:
        -id: (int) dataset id, or `None` for no dataset
    """
    if external_id:
        client = global_client["files"]
        dataset = client.data_sets.retrieve(external_id=external_id)        
        return dataset.id
    else:
        return None


def file_to_dataset(file_external_id, dataset_external_id):
    """
    Assign a file to a dataset.
    Input
        - file_external_id: (str) the file's external id 
        - dataset_external_id: (str) the dataset's external id, `None` for no
            dataset
    """
    client = global_client["files"]
    dataset_id = get_dataset_id(dataset_external_id)
    file_metadata_update = FileMetadataUpdate(external_id=file_external_id)
    file_metadata_update = file_metadata_update.data_set_id.set(dataset_id)
    _ = client.files.update(file_metadata_update)
    logging.info(f"Assigned dataset {dataset_id} to file {file_external_id}")

