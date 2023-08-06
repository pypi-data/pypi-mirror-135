# agilicus_api.ServicesApi

All URIs are relative to *https://api.agilicus.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_service**](ServicesApi.md#create_service) | **POST** /v2/services | Create a Service
[**delete_service**](ServicesApi.md#delete_service) | **DELETE** /v2/services/{service_id} | Remove a Service
[**get_service**](ServicesApi.md#get_service) | **GET** /v2/services/{service_id} | Get a single Service
[**list_services**](ServicesApi.md#list_services) | **GET** /v2/services | Get a subset of the Services
[**replace_service**](ServicesApi.md#replace_service) | **PUT** /v2/services/{service_id} | Create or update a Service.


# **create_service**
> Service create_service(service)

Create a Service

Creates a new Service. Note that the Service's name must be unique across all other services an Applications, regardless of the Organisation. 

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import services_api
from agilicus_api.model.service import Service
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = services_api.ServicesApi(api_client)
    service = Service(
        name="name_example",
        description="description_example",
        org_id="org_id_example",
        contact_email="contact_email_example",
        roles=RoleList([
            Role(
                name="name_example",
                rules=[
                    Rule(
                        host="host_example",
                        name="rules.add",
                        method="get",
                        path="/.*",
                        query_parameters=[
                            RuleQueryParameter(
                                name="name_example",
                                exact_match="exact_match_example",
                            ),
                        ],
                        body=RuleQueryBody(
                            json=[
                                RuleQueryBodyJSON(
                                    name="name_example",
                                    exact_match="exact_match_example",
                                    match_type="string",
                                    pointer="/foo/0/a~1b/2",
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ]),
        definitions=[
            Definition(
                key="key_example",
                value="value_example",
            ),
        ],
        base_url="api.agilicus.com/v1",
    ) # Service | 

    # example passing only required values which don't have defaults set
    try:
        # Create a Service
        api_response = api_instance.create_service(service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->create_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service** | [**Service**](Service.md)|  |

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | New Service created |  -  |
**409** | A Service with the same name already exists for this organisation. The existing Service is returned.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service**
> delete_service(service_id, org_id)

Remove a Service

Remove a Service

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import services_api
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = services_api.ServicesApi(api_client)
    service_id = "G" # str | Service unique identifier
    org_id = "G" # str | Organisation unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Remove a Service
        api_instance.delete_service(service_id, org_id)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->delete_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier |
 **org_id** | **str**| Organisation unique identifier |

### Return type

void (empty response body)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Service was deleted |  -  |
**404** | Service does not exist |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service**
> Service get_service(service_id)

Get a single Service

Get a single Service

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import services_api
from agilicus_api.model.service import Service
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = services_api.ServicesApi(api_client)
    service_id = "G" # str | Service unique identifier

    # example passing only required values which don't have defaults set
    try:
        # Get a single Service
        api_response = api_instance.get_service(service_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->get_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier |

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Service was found. |  -  |
**404** | The Service does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_services**
> ListServicesResponse list_services()

Get a subset of the Services

Retrieves all Services owned by the Organisation.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import services_api
from agilicus_api.model.list_services_response import ListServicesResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = services_api.ServicesApi(api_client)
    org_id = "1234" # str | Organisation Unique identifier (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a subset of the Services
        api_response = api_instance.list_services(org_id=org_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->list_services: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | **str**| Organisation Unique identifier | [optional]

### Return type

[**ListServicesResponse**](ListServicesResponse.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The list of retrieved Services |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_service**
> Service replace_service(service_id)

Create or update a Service.

Create or update a Service.

### Example

* Bearer (JWT) Authentication (token-valid):
```python
import time
import agilicus_api
from agilicus_api.api import services_api
from agilicus_api.model.service import Service
from agilicus_api.model.error_message import ErrorMessage
from pprint import pprint
# Defining the host is optional and defaults to https://api.agilicus.com
# See configuration.py for a list of all supported configuration parameters.
configuration = agilicus_api.Configuration(
    host = "https://api.agilicus.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): token-valid
configuration = agilicus_api.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with agilicus_api.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = services_api.ServicesApi(api_client)
    service_id = "G" # str | Service unique identifier
    service = Service(
        name="name_example",
        description="description_example",
        org_id="org_id_example",
        contact_email="contact_email_example",
        roles=RoleList([
            Role(
                name="name_example",
                rules=[
                    Rule(
                        host="host_example",
                        name="rules.add",
                        method="get",
                        path="/.*",
                        query_parameters=[
                            RuleQueryParameter(
                                name="name_example",
                                exact_match="exact_match_example",
                            ),
                        ],
                        body=RuleQueryBody(
                            json=[
                                RuleQueryBodyJSON(
                                    name="name_example",
                                    exact_match="exact_match_example",
                                    match_type="string",
                                    pointer="/foo/0/a~1b/2",
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ]),
        definitions=[
            Definition(
                key="key_example",
                value="value_example",
            ),
        ],
        base_url="api.agilicus.com/v1",
    ) # Service |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create or update a Service.
        api_response = api_instance.replace_service(service_id)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->replace_service: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create or update a Service.
        api_response = api_instance.replace_service(service_id, service=service)
        pprint(api_response)
    except agilicus_api.ApiException as e:
        print("Exception when calling ServicesApi->replace_service: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_id** | **str**| Service unique identifier |
 **service** | [**Service**](Service.md)|  | [optional]

### Return type

[**Service**](Service.md)

### Authorization

[token-valid](../README.md#token-valid)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The Service was updated. Returns the latest version of it after the update was applied.  |  -  |
**404** | Service does not exist. |  -  |
**409** | The provided Service conflicted with the value stored in the API. Please fetch the latest version and try again with it.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

