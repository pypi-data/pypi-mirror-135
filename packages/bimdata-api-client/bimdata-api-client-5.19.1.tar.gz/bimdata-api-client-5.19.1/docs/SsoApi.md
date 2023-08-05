# bimdata_api_client.SsoApi

All URIs are relative to *https://api.bimdata.io*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accept_invitation**](SsoApi.md#accept_invitation) | **POST** /identity-provider/invitation/{id}/accept | Accept an invitation
[**delete_user**](SsoApi.md#delete_user) | **DELETE** /identity-provider/user | Delete user from BIMData
[**deny_invitation**](SsoApi.md#deny_invitation) | **POST** /identity-provider/invitation/{id}/deny | Deny an invitation
[**get_invitation**](SsoApi.md#get_invitation) | **GET** /identity-provider/invitation/{id} | Retrieve an invitation
[**get_invitations**](SsoApi.md#get_invitations) | **GET** /identity-provider/invitation | Retrieve all invitations


# **accept_invitation**
> accept_invitation(id)

Accept an invitation

If the user already exists, s·he is added to the cloud and projet. If not, we wait their first connection to add them. Required scopes: org:manage

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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Accept an invitation
        api_instance.accept_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->accept_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Accept an invitation
        api_instance.accept_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->accept_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Accept an invitation
        api_instance.accept_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->accept_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. | 

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
**204** | empty |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> delete_user(data)

Delete user from BIMData

NON HANDLED EDGE CASE: The user has been created on the identity provider (exists on the IDP) The user (or an app) has requested an access token (exists on keycloak) But the user has never used the API (doesn't exist on the API) So the API can't delete the user and can't forward the call to keycloak so a zombie user will stay on keycloak

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
    api_instance = bimdata_api_client.SsoApi(api_client)
    data = bimdata_api_client.SelectUser() # SelectUser | 

    try:
        # Delete user from BIMData
        api_instance.delete_user(data)
    except ApiException as e:
        print("Exception when calling SsoApi->delete_user: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    data = bimdata_api_client.SelectUser() # SelectUser | 

    try:
        # Delete user from BIMData
        api_instance.delete_user(data)
    except ApiException as e:
        print("Exception when calling SsoApi->delete_user: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    data = bimdata_api_client.SelectUser() # SelectUser | 

    try:
        # Delete user from BIMData
        api_instance.delete_user(data)
    except ApiException as e:
        print("Exception when calling SsoApi->delete_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**SelectUser**](SelectUser.md)|  | 

### Return type

void (empty response body)

### Authorization

[Bearer](../README.md#Bearer), [bimdata_connect](../README.md#bimdata_connect), [client_credentials](../README.md#client_credentials)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | empty |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deny_invitation**
> deny_invitation(id)

Deny an invitation

The invitation status change to DENIED and the user is not added to the cloud. You can accept an invitation previously denied Required scopes: org:manage

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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Deny an invitation
        api_instance.deny_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->deny_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Deny an invitation
        api_instance.deny_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->deny_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Deny an invitation
        api_instance.deny_invitation(id)
    except ApiException as e:
        print("Exception when calling SsoApi->deny_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. | 

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
**204** | empty |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_invitation**
> Invitation get_invitation(id)

Retrieve an invitation

Retrieve all invitations of your identity provider Required scopes: org:manage

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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Retrieve an invitation
        api_response = api_instance.get_invitation(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Retrieve an invitation
        api_response = api_instance.get_invitation(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitation: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    id = 56 # int | A unique integer value identifying this invitation.

    try:
        # Retrieve an invitation
        api_response = api_instance.get_invitation(id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. | 

### Return type

[**Invitation**](Invitation.md)

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

# **get_invitations**
> list[Invitation] get_invitations(status=status)

Retrieve all invitations

Retrieve all invitations of your identity provider Required scopes: org:manage

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
    api_instance = bimdata_api_client.SsoApi(api_client)
    status = 'status_example' # str | Filter the returned list by status (optional)

    try:
        # Retrieve all invitations
        api_response = api_instance.get_invitations(status=status)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitations: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    status = 'status_example' # str | Filter the returned list by status (optional)

    try:
        # Retrieve all invitations
        api_response = api_instance.get_invitations(status=status)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitations: %s\n" % e)
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
    api_instance = bimdata_api_client.SsoApi(api_client)
    status = 'status_example' # str | Filter the returned list by status (optional)

    try:
        # Retrieve all invitations
        api_response = api_instance.get_invitations(status=status)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SsoApi->get_invitations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**| Filter the returned list by status | [optional] 

### Return type

[**list[Invitation]**](Invitation.md)

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

