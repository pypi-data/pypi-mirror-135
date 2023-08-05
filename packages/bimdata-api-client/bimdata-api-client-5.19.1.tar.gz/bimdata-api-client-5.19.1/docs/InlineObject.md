# InlineObject

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**parent_id** | **int** |  | [optional] 
**type** | **str** | Value is \&quot;Folder\&quot;. It is usefull to parse the tree and discriminate folders and files | [optional] [readonly] 
**name** | **str** | Name of the folder | 
**created_at** | **datetime** | Creation date | [optional] [readonly] 
**updated_at** | **datetime** | Date of the last update | [optional] [readonly] 
**created_by** | [**User**](User.md) |  | [optional] 
**groups_permissions** | [**list[FolderGroupPermission]**](FolderGroupPermission.md) |  | [optional] [readonly] 
**default_permission** | **int** | Permission for a Folder | [optional] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


