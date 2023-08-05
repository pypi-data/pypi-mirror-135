# RecursiveFolderChildren

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**parent_id** | **int** |  | 
**created_by** | [**User**](User.md) |  | [optional] 
**creator** | [**User**](User.md) |  | [optional] 
**type** | **str** | Values can be &#39;Folder&#39;, &#39;Document&#39; or &#39;Ifc&#39;. It is usefull to parse the tree and discriminate folders and files | [optional] [readonly] 
**name** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**file_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**ifc_id** | **int** |  | [optional] [readonly] 
**file** | **str** |  | [optional] [readonly] 
**groups_permissions** | [**list[FolderGroupPermission]**](FolderGroupPermission.md) | Groups permissions of folder | [optional] [readonly] 
**default_permission** | **int** | Default permissions of folder | [optional] [readonly] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [optional] [readonly] 
**children** | [**list[RecursiveFolderChildren]**](RecursiveFolderChildren.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


