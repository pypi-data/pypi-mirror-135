# MarketplaceApp

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**name** | **str** |  | 
**short_description** | **str** |  | 
**long_description** | **str** |  | 
**activation_webhook_url** | **str** |  | [optional] 
**post_activation_redirect_uri** | **str** |  | [optional] 
**viewer_plugins_urls** | **list[str]** |  | [optional] 
**webhook_secret** | **str** |  | [optional] 
**creator** | [**User**](User.md) |  | [optional] 
**scopes** | **list[str]** |  | [optional] [readonly] 
**settings_url** | **str** | this URL will be called with query params ?cloud_id&#x3D; | [optional] 
**is_public** | **bool** |  | [optional] 
**tags** | **list[str]** |  | [optional] 
**logo** | **str** |  | [optional] [readonly] 
**images** | [**list[MarketplaceAppImage]**](MarketplaceAppImage.md) |  | [optional] [readonly] 
**organization** | [**PublicOrganization**](PublicOrganization.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


