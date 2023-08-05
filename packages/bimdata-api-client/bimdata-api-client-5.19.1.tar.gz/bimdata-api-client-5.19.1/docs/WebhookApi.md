# bimdata_api_client.WebhookApi

All URIs are relative to *https://api.bimdata.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_web_hook**](WebhookApi.md#create_web_hook) | **POST** /cloud/{cloud_pk}/webhook | Create a new Webhook
[**delete_web_hook**](WebhookApi.md#delete_web_hook) | **DELETE** /cloud/{cloud_pk}/webhook/{id} | Delete a webhook
[**get_web_hook**](WebhookApi.md#get_web_hook) | **GET** /cloud/{cloud_pk}/webhook/{id} | Retrieve one configured webhook
[**get_web_hooks**](WebhookApi.md#get_web_hooks) | **GET** /cloud/{cloud_pk}/webhook | Retrieve all configured webhooks
[**ping_web_hook**](WebhookApi.md#ping_web_hook) | **POST** /cloud/{cloud_pk}/webhook/{id}/ping | Test a webhook
[**update_web_hook**](WebhookApi.md#update_web_hook) | **PATCH** /cloud/{cloud_pk}/webhook/{id} | Update some field of a webhook


# **create_web_hook**
> WebHook create_web_hook(cloud_pk, data)

Create a new Webhook

Create a new Webhook Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Create a new Webhook
        api_response = api_instance.create_web_hook(cloud_pk, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->create_web_hook: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Create a new Webhook
        api_response = api_instance.create_web_hook(cloud_pk, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->create_web_hook: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Create a new Webhook
        api_response = api_instance.create_web_hook(cloud_pk, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->create_web_hook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 
 **data** | [**WebHook**](WebHook.md)|  | 

### Return type

[**WebHook**](WebHook.md)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_web_hook**
> delete_web_hook(cloud_pk, id)

Delete a webhook

Delete a webhook Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Delete a webhook
        api_instance.delete_web_hook(cloud_pk, id)
    except ApiException as e:
        print("Exception when calling WebhookApi->delete_web_hook: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Delete a webhook
        api_instance.delete_web_hook(cloud_pk, id)
    except ApiException as e:
        print("Exception when calling WebhookApi->delete_web_hook: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Delete a webhook
        api_instance.delete_web_hook(cloud_pk, id)
    except ApiException as e:
        print("Exception when calling WebhookApi->delete_web_hook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_hook**
> WebHook get_web_hook(cloud_pk, id)

Retrieve one configured webhook

Retrieve one configured webhook Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Retrieve one configured webhook
        api_response = api_instance.get_web_hook(cloud_pk, id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hook: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Retrieve one configured webhook
        api_response = api_instance.get_web_hook(cloud_pk, id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hook: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 

    try:
        # Retrieve one configured webhook
        api_response = api_instance.get_web_hook(cloud_pk, id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**WebHook**](WebHook.md)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_hooks**
> list[WebHook] get_web_hooks(cloud_pk)

Retrieve all configured webhooks

Retrieve all configured webhooks Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 

    try:
        # Retrieve all configured webhooks
        api_response = api_instance.get_web_hooks(cloud_pk)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hooks: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 

    try:
        # Retrieve all configured webhooks
        api_response = api_instance.get_web_hooks(cloud_pk)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hooks: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 

    try:
        # Retrieve all configured webhooks
        api_response = api_instance.get_web_hooks(cloud_pk)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->get_web_hooks: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 

### Return type

[**list[WebHook]**](WebHook.md)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping_web_hook**
> WebHook ping_web_hook(cloud_pk, id, data)

Test a webhook

Trigger a Ping Event sending {\"ok\": true} to the webhook URL. Useful to test your app Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Test a webhook
        api_response = api_instance.ping_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->ping_web_hook: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Test a webhook
        api_response = api_instance.ping_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->ping_web_hook: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Test a webhook
        api_response = api_instance.ping_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->ping_web_hook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 
 **id** | **str**|  | 
 **data** | [**WebHook**](WebHook.md)|  | 

### Return type

[**WebHook**](WebHook.md)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_web_hook**
> WebHook update_web_hook(cloud_pk, id, data)

Update some field of a webhook

Update some field of a webhook Required scopes: webhook:manage

### Example

* Api Key Authentication (Bearer):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Update some field of a webhook
        api_response = api_instance.update_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->update_web_hook: %s\n" % e)
```

* OAuth Authentication (bimdata_connect):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Update some field of a webhook
        api_response = api_instance.update_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->update_web_hook: %s\n" % e)
```

* OAuth Authentication (client_credentials):
```python
from __future__ import print_function
import time
import bimdata_api_client
from bimdata_api_client.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.bimdata.io
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: Bearer
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io",
    api_key = {
        'Authorization': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# Configure OAuth2 access token for authorization: bimdata_connect
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: client_credentials
configuration = bimdata_api_client.Configuration(
    host = "https://api.bimdata.io"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = bimdata_api_client.WebhookApi(api_client)
    cloud_pk = 'cloud_pk_example' # str | 
id = 'id_example' # str | 
data = bimdata_api_client.WebHook() # WebHook | 

    try:
        # Update some field of a webhook
        api_response = api_instance.update_web_hook(cloud_pk, id, data)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WebhookApi->update_web_hook: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **str**|  | 
 **id** | **str**|  | 
 **data** | [**WebHook**](WebHook.md)|  | 

### Return type

[**WebHook**](WebHook.md)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

