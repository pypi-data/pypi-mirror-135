# Visa

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**validations** | [**list[VisaValidation]**](VisaValidation.md) |  | [optional] [readonly] 
**validations_in_error** | **list[int]** | Validation IDs where one or more validators have no longer access to the visa document. | [optional] [readonly] 
**creator** | [**UserProject**](UserProject.md) |  | [optional] 
**creator_id** | **int** | This is the userproject_id. This field is only used if the call is made from an App | [optional] 
**status** | **str** |  | [optional] [readonly] 
**description** | **str** | Description of the visa | [optional] 
**document** | [**Document**](Document.md) |  | [optional] 
**comments** | [**list[VisaComment]**](VisaComment.md) |  | [optional] [readonly] 
**deadline** | **date** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


