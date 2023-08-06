# sust.api.climate_explorer.clientgen.PortfoliosApi

All URIs are relative to *https://explorer.sustglobal.io/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**portfolios_assets_export_list**](PortfoliosApi.md#portfolios_assets_export_list) | **GET** /portfolios/{portfolio_name}/assets/export | Export Portfolio Assets
[**portfolios_assets_import_create**](PortfoliosApi.md#portfolios_assets_import_create) | **POST** /portfolios/{portfolio_name}/assets/import | Import Portfolio Assets
[**portfolios_assets_list**](PortfoliosApi.md#portfolios_assets_list) | **GET** /portfolios/{portfolio_name}/assets | List Portfolio Assets
[**portfolios_create**](PortfoliosApi.md#portfolios_create) | **POST** /portfolios/ | Create Portfolio
[**portfolios_datasets_physical_export_list**](PortfoliosApi.md#portfolios_datasets_physical_export_list) | **GET** /portfolios/{portfolio_name}/datasets/physical/export | Export Physical Risk Exposure Dataset
[**portfolios_datasets_physical_items_list**](PortfoliosApi.md#portfolios_datasets_physical_items_list) | **GET** /portfolios/{portfolio_name}/datasets/physical/items | Get Physical Risk Exposure Data
[**portfolios_datasets_physical_list**](PortfoliosApi.md#portfolios_datasets_physical_list) | **GET** /portfolios/{portfolio_name}/datasets/physical | Get Physical Risk Exposure Metadata
[**portfolios_datasets_physical_summary_list**](PortfoliosApi.md#portfolios_datasets_physical_summary_list) | **GET** /portfolios/{portfolio_name}/datasets/physical/summary | Get Physical Risk Exposure Summary
[**portfolios_delete**](PortfoliosApi.md#portfolios_delete) | **DELETE** /portfolios/{portfolio_name}/ | Delete Portfolio
[**portfolios_list**](PortfoliosApi.md#portfolios_list) | **GET** /portfolios/ | List Portfolios
[**portfolios_read**](PortfoliosApi.md#portfolios_read) | **GET** /portfolios/{portfolio_name}/ | Get Portfolio


# **portfolios_assets_export_list**
> file_type portfolios_assets_export_list(portfolio_name)

Export Portfolio Assets

Trigger an export operation of portfolio assets.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Export Portfolio Assets
        api_response = api_instance.portfolios_assets_export_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_export_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Export Portfolio Assets
        api_response = api_instance.portfolios_assets_export_list(portfolio_name, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_export_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

**file_type**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * Content-Disposition - Indicates the response contains an &#39;attachment&#39; with a human-friendly name <br>  * Content-Type - Media type describing the attached file <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_assets_import_create**
> MessageResponse portfolios_assets_import_create(portfolio_name, asset)

Import Portfolio Assets

Trigger an import operation of assets into existing portfolio. Format of the required CSV file is documented at https://developers.sustglobal.com/explorer.html.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.message_response import MessageResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    asset = open('/path/to/file', 'rb') # file_type | CSV file containing portfolio assets
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Import Portfolio Assets
        api_response = api_instance.portfolios_assets_import_create(portfolio_name, asset)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_import_create: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Import Portfolio Assets
        api_response = api_instance.portfolios_assets_import_create(portfolio_name, asset, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_import_create: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **asset** | **file_type**| CSV file containing portfolio assets |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_assets_list**
> [AssetResponse] portfolios_assets_list(portfolio_name)

List Portfolio Assets

Retrieve a set of assets belonging to a specific portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.asset_response import AssetResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)
    rows = 1 # int | Maximum number of items to return per page (min=1, max=250) (optional)
    page = 1 # int | Numerical index of current page, beginning at 1 (optional)

    # example passing only required values which don't have defaults set
    try:
        # List Portfolio Assets
        api_response = api_instance.portfolios_assets_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List Portfolio Assets
        api_response = api_instance.portfolios_assets_list(portfolio_name, project=project, rows=rows, page=page)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_assets_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]
 **rows** | **int**| Maximum number of items to return per page (min&#x3D;1, max&#x3D;250) | [optional]
 **page** | **int**| Numerical index of current page, beginning at 1 | [optional]

### Return type

[**[AssetResponse]**](AssetResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_create**
> PortfolioResponse portfolios_create(data)

Create Portfolio

Create an empty portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.portfolio_response import PortfolioResponse
from sust.api.climate_explorer.clientgen.model.portfolio_create_request import PortfolioCreateRequest
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    data = PortfolioCreateRequest(
        portfolio_name="portfolio_name_example",
    ) # PortfolioCreateRequest | 
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create Portfolio
        api_response = api_instance.portfolios_create(data)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_create: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create Portfolio
        api_response = api_instance.portfolios_create(data, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_create: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**PortfolioCreateRequest**](PortfolioCreateRequest.md)|  |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**PortfolioResponse**](PortfolioResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_datasets_physical_export_list**
> file_type portfolios_datasets_physical_export_list(portfolio_name)

Export Physical Risk Exposure Dataset

Trigger an export operation of physical risk exposure data.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Export Physical Risk Exposure Dataset
        api_response = api_instance.portfolios_datasets_physical_export_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_export_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Export Physical Risk Exposure Dataset
        api_response = api_instance.portfolios_datasets_physical_export_list(portfolio_name, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_export_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

**file_type**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  * Content-Disposition - Indicates the response contains an &#39;attachment&#39; with a human-friendly name <br>  * Content-Type - Media type describing the attached file <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_datasets_physical_items_list**
> [PhysicalRiskDatasetItemResponse] portfolios_datasets_physical_items_list(portfolio_name)

Get Physical Risk Exposure Data

Retrieve items from the physical risk exposure dataset generated for a portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.physical_risk_dataset_item_response import PhysicalRiskDatasetItemResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)
    risk_type = "fire" # str | Climate hazard filter (optional)
    start_date = "start_date_example" # str | Left boundary of time range filter in format YYYY-MM-DD (optional)
    end_date = "end_date_example" # str | Right boundary of time range filter in format YYYY-MM-DD (optional)
    rows = 1 # int | Maximum number of items to return per page (min=1, max=250) (optional)
    page = 1 # int | Numerical index of current page, beginning at 1 (optional)
    scenario = "ssp126" # str | Shared socioeconomic pathway filter (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Physical Risk Exposure Data
        api_response = api_instance.portfolios_datasets_physical_items_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_items_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Physical Risk Exposure Data
        api_response = api_instance.portfolios_datasets_physical_items_list(portfolio_name, project=project, risk_type=risk_type, start_date=start_date, end_date=end_date, rows=rows, page=page, scenario=scenario)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_items_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]
 **risk_type** | **str**| Climate hazard filter | [optional]
 **start_date** | **str**| Left boundary of time range filter in format YYYY-MM-DD | [optional]
 **end_date** | **str**| Right boundary of time range filter in format YYYY-MM-DD | [optional]
 **rows** | **int**| Maximum number of items to return per page (min&#x3D;1, max&#x3D;250) | [optional]
 **page** | **int**| Numerical index of current page, beginning at 1 | [optional]
 **scenario** | **str**| Shared socioeconomic pathway filter | [optional]

### Return type

[**[PhysicalRiskDatasetItemResponse]**](PhysicalRiskDatasetItemResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_datasets_physical_list**
> PhysicalRiskMetadataResponse portfolios_datasets_physical_list(portfolio_name)

Get Physical Risk Exposure Metadata

Retrieve metadata from the physical risk exposure dataset generated for a portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.physical_risk_metadata_response import PhysicalRiskMetadataResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Physical Risk Exposure Metadata
        api_response = api_instance.portfolios_datasets_physical_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Physical Risk Exposure Metadata
        api_response = api_instance.portfolios_datasets_physical_list(portfolio_name, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**PhysicalRiskMetadataResponse**](PhysicalRiskMetadataResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_datasets_physical_summary_list**
> [PhysicalRiskDatasetSummaryResponse] portfolios_datasets_physical_summary_list(portfolio_name)

Get Physical Risk Exposure Summary

Retrieve a summary of the physical risk exposure dataset generated for a portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.physical_risk_dataset_summary_response import PhysicalRiskDatasetSummaryResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | Name for portfolio
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)
    rows = 1 # int | Maximum number of items to return per page (min=1, max=250) (optional)
    page = 1 # int | Numerical index of current page, beginning at 1 (optional)
    scenario = "ssp126" # str | Shared socioeconomic pathway filter (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Physical Risk Exposure Summary
        api_response = api_instance.portfolios_datasets_physical_summary_list(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_summary_list: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Physical Risk Exposure Summary
        api_response = api_instance.portfolios_datasets_physical_summary_list(portfolio_name, project=project, rows=rows, page=page, scenario=scenario)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_datasets_physical_summary_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**| Name for portfolio |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]
 **rows** | **int**| Maximum number of items to return per page (min&#x3D;1, max&#x3D;250) | [optional]
 **page** | **int**| Numerical index of current page, beginning at 1 | [optional]
 **scenario** | **str**| Shared socioeconomic pathway filter | [optional]

### Return type

[**[PhysicalRiskDatasetSummaryResponse]**](PhysicalRiskDatasetSummaryResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_delete**
> MessageResponse portfolios_delete(portfolio_name)

Delete Portfolio

Deletes a portfolio and all associated Risk Exposure Data.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.message_response import MessageResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | 
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Portfolio
        api_response = api_instance.portfolios_delete(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_delete: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Portfolio
        api_response = api_instance.portfolios_delete(portfolio_name, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**|  |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_list**
> [PortfolioResponse] portfolios_list()

List Portfolios

Retrieve a list of portfolios.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.portfolio_response import PortfolioResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List Portfolios
        api_response = api_instance.portfolios_list(project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_list: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**[PortfolioResponse]**](PortfolioResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portfolios_read**
> PortfolioResponse portfolios_read(portfolio_name)

Get Portfolio

Retrieve a single portfolio.

### Example

* Api Key Authentication (api_key):

```python
import time
import sust.api.climate_explorer.clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api
from sust.api.climate_explorer.clientgen.model.portfolio_response import PortfolioResponse
from pprint import pprint
# Defining the host is optional and defaults to https://explorer.sustglobal.io/api
# See configuration.py for a list of all supported configuration parameters.
configuration = sust.api.climate_explorer.clientgen.Configuration(
    host = "https://explorer.sustglobal.io/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with sust.api.climate_explorer.clientgen.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = portfolios_api.PortfoliosApi(api_client)
    portfolio_name = "portfolio_name_example" # str | 
    project = "project_example" # str | Name of project. Param only required when user may access more than one. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Portfolio
        api_response = api_instance.portfolios_read(portfolio_name)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_read: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Portfolio
        api_response = api_instance.portfolios_read(portfolio_name, project=project)
        pprint(api_response)
    except sust.api.climate_explorer.clientgen.ApiException as e:
        print("Exception when calling PortfoliosApi->portfolios_read: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portfolio_name** | **str**|  |
 **project** | **str**| Name of project. Param only required when user may access more than one. | [optional]

### Return type

[**PortfolioResponse**](PortfolioResponse.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

