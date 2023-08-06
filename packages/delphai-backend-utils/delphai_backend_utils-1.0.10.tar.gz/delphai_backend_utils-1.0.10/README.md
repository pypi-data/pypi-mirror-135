# Delphai backend common facilities [Pakage]

## Development
Github action deploys to pypi when a new tag is created.
Also make sure the version in ```setup.py``` is equal to the version on Github

**NOTE** PYPI wont allow version overriding, Means make sure the pakage works well before changing the version in ```setup.py```


## Installation
Include the reference to this library into your <code>Pipfile</code>
```conf
[packages]
delphai-backend-utils = "*"
```
The following packages will be installed automatically, and you do not need to include them into <code>Pipfile</code>:
- omegaconf = "*"
- memoization = "*"
- azure-identity = "==1.4.0b3"
- azure-keyvault = "*"
- python-dotenv = "*"
- kubernetes = "*"
- coloredlogs = "*"

If you are going to use the module **db_access**, please also include <code>pymongo</code> into <code>Pipfile</code>:
```conf
[packages]
delphai-backend-utils = "*"
pymongo = "*"
```
If you are going to use the module **grpc_calls**, please also include gRPC dependencies into <code>Pipfile</code>:
```conf
[packages]
delphai-backend-utils = "*"
grpcio-reflection = "*"
```
For full functionality:
```conf
[packages]
delphai-backend-utils = "*"
pymongo = "*"
grpcio = "*"
grpcio-tools = "*"
grpcio-reflection = "*"
tornado = "*"
```
To update this library in your development environment:
```shell
pipenv update
```
## Module **config**
Loads and provides configuration data from <code>config/*.yml</code> files, including resolved values from environment variables stored into <code>.env</code> file, and Kubernetes and Azure secrets.

Configuration files used to compile an actual working configuration:
- config/**default.yml** - basic default configuration
- config/**development.yml** - redefines default configuration in a development environment
- config/**review.yml** - redefines default configuration in the review environment
- config/**staging.yml** - redefines default configuration in the staging environment
- config/**production.yml** - redefines default configuration in the production environment
- **.env** - used only in development environment

**Importing:**
```python
from delphai_backend_utils.config import get_config
```
**Usage example 1** - retrieving a single value:
```python
    address = get_config('server.host_and_port')
```
If value is not redefined in a environment-specific config file, it will be extracted from default.yml:
```yml
server:
  host_and_port: 0.0.0.0:8080
```
**Usage example 2** - retrieving and using a whole chapter:
```python
    server_config = get_config('server')
    address = server_config['host_and_port']  # Be careful, a KeyError might happen
```
**Usage example 3** - retrieving the whole configuraion as an OmegaConf object:
```python
    config = get_config(None)  # Notice "None"
    db_name = config.db.name  # "MissingMandatoryValue: Missing mandatory value: db.connection_string" can happen, and it might be a desirable behavior
```
## Module **db_config**
Establishing connections to MongoDB.

**Importing:**
```python
from delphai_backend_utils.db_config import get_own_db_connection
```
Please **do not forget** to include <code>pymongo</code> into your <code>Pipfile</code> (see above in the "Installation" section).

**Usage example** - printing out a "companies" collection size:
```python
    db_conn = get_own_db_connection()
    print(db_conn.companies.estimated_document_count())
```
There is one more function <code>chunks</code> in this module which is hugely useful when we need to implement chunked reads and updates.
## Module **logging**
Configurable logging. In addition to standard logging operations implements <code>error_with_traceback</code> function that logs a last occured exception.

**Importing:**
```python
from delphai_backend_utils import logging
```
**Usage example** - printing out a "companies" collection size:
```python
from delphai_backend_utils import logging

def fail_here():
    return 1/0

def calculate_result():
    try:
        return fail_here()
    except Exception:
        logging.error_with_traceback()
        return None
```
## Module **grpc_calls**
The natural way to call other microservices. Functions:
- call_grpc - calls other grpc service
- async_call_grpc - awaitable version of call_grpc. Use if caller is "async def".
- get_description - to get other grpc's service description
- async_get_description - awaitable version of get_description. Use if caller is "async def".

**Importing:**
```python
from delphai_backend_utils import grpc_calls
```
Please **do not forget** to include gRPC dependencies into your <code>Pipfile</code> (see above in the "Installatio" section).

**Usage example** - printing out a "companies" collection size:
```python
    suggestions = grpc_calls.call_grpc('delphai.typeahead.Typeahead.get_suggestions', {'search_query': 'siemens'})
    for idx, suggestion in enumerate(suggestions['matches']):
        print(f'{idx + 1}. {suggestion["value"]} {suggestion.get("url")}')
```
## Module **users**
The natural way to call other microservices. Functions:
- call_grpc - calls other grpc service
- async_call_grpc - awaitable version of call_grpc. Use if caller is "async def".
- get_description - to get other grpc's service description
- async_get_description - awaitable version of get_description. Use if caller is "async def".

**Importing:**
```python
from delphai_backend_utils.user import get_user
```
**Usage example**:
```python
    try:
        user = get_user(context)  # context is a gRPC context that usually contains user description in its metadata
        user_id_str = user.get('https://delphai.com/mongo_user_id')
    except Exception:
        raise Exception('Failed get user info')
    if not user_id_str:
        raise Exception('User profile is not properly configured')
```


## Module **formatting**
Common forms and formatting standards. Functions:
- clean_url - clean an url

**Importing:**
```python
from delphai_backend_utils.formatting import clean_url
```
**Usage example**:
```python
    url = clean_url(url, keep_www=True)  
```

## Module **own_gateway**
Implements an individual HTTP1&ndash;&gt;gRPC (HTTP2) gateway for gRPC microservices.

**Usage example** (<code>serve</code> function in <code>server.py</code> module):
```python
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_GreetingServicer_to_server(Greeting(), server)

    # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    service_names = (
        service_pb2.DESCRIPTOR.services_by_name['Greeting'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)

    # Start own gateway if configured                                  # <<<<
    run_own_gateway = get_config('server.run_own_gateway') or False    # <<<<
    if run_own_gateway:                                                # <<<<
        from delphai_backend_utils.own_gateway import run_own_gateway  # <<<<
        run_own_gateway(service_pb2.DESCRIPTOR, server)                # <<<<

    address = get_config('server.host_and_port') or '0.0.0.0:8080'
    server.add_insecure_port(address)
    server.start()
    logging.info(f'Started server {address}')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.error('Interrupted')
```
Lines to add marked with "<code># &lt;&lt;&lt;&lt;</code>".

**Additionally**:
1. Include <code>tornado</code> into your <code>Pipfile</code> (see above in the "Installation" section).
2. Turn on this feature in your configuration file (<code>default.yml</code> or some other configuration file):
```yaml
server:
  # host_and_port: 0.0.0.0:8080  # "0.0.0.0:8080" is a default value. Uncomment and change if you need another.
  run_own_gateway: true  # Set to true if you need an individual gateway to be runned together with gRPC handler.
  # gateway_host_and_port: 0.0.0.0:7070  # "0.0.0.0:7070" is a default value.
```

## Module **api_calls**
A wrapper for calling APIs. Contains only a single function for Azure Machine Learning Endpoints right now (`call_azure_endpoint`).

**Importing:**
```python
from delphai_backend_utils.api_calls import call_azure_endpoint
```

**Usage example** - calling word embedding model to retrieve similar keywords:
```python
    api_url = 'http://51.145.149.205:80/api/v1/service/similar-keywords/score'
    api_key = ''  # has to be set
    keywords_resp = call_azure_endpoint(api_url, api_key, 'urban mobility')
    if keywords_resp['success']:
        print(', '.join([keyword for keyword, _ in keywords_resp['content']]))
```
