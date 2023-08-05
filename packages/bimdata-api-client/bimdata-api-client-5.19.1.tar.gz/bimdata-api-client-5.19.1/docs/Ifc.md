# Ifc

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**name** | **str** |  | [optional] [readonly] 
**type** | **str** |  | [optional] [readonly] 
**creator** | [**User**](User.md) |  | [optional] 
**status** | **str** |  | [optional] [readonly] 
**source** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**document_id** | **str** |  | [optional] [readonly] 
**document** | [**Document**](Document.md) |  | [optional] 
**structure_file** | **str** |  | [optional] [readonly] 
**systems_file** | **str** |  | [optional] [readonly] 
**map_file** | **str** |  | [optional] [readonly] 
**gltf_file** | **str** |  | [optional] [readonly] 
**bvh_tree_file** | **str** |  | [optional] [readonly] 
**viewer_360_file** | **str** |  | [optional] [readonly] 
**xkt_file** | **str** |  | [optional] [readonly] 
**project_id** | **str** |  | [optional] [readonly] 
**world_position** | **list[float]** | [x,y,z] array of the position of the local_placement in world coordinates | [optional] 
**errors** | **list[str]** | List of errors that happened during IFC processing | [optional] [readonly] 
**warnings** | **list[str]** | List of warnings that happened during IFC processing | [optional] [readonly] 
**archived** | **bool** |  | [optional] 
**version** | **str** | This field is only for information. Updating it won&#39;t impact the export. | [optional] 
**north_vector** | **list[list[float]]** | This field is only for information. Updating it won&#39;t impact the export. | [optional] 
**recommanded_2d_angle** | **float** | This is the angle in clockwise degree to apply on the 2D to optimise the horizontality of objects. This field is only for information. Updating it won&#39;t impact the export. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


