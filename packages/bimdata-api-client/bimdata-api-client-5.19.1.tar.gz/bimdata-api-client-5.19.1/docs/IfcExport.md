# IfcExport

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**classifications** | **str** | Exported IFC will include classifications from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include classifications(NONE) | [optional] [default to 'UPDATED']
**zones** | **str** | Exported IFC will include zones from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include zones(NONE) | [optional] [default to 'UPDATED']
**properties** | **str** | Exported IFC will include properties from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include properties(NONE) | [optional] [default to 'UPDATED']
**systems** | **str** | Exported IFC will include systems from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include systems(NONE) | [optional] [default to 'UPDATED']
**layers** | **str** | Exported IFC will include layers from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include layers(NONE) | [optional] [default to 'UPDATED']
**materials** | **str** | Exported IFC will include materials from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include materials(NONE) | [optional] [default to 'UPDATED']
**attributes** | **str** | Exported IFC will include attributes from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include attributes(NONE) | [optional] [default to 'UPDATED']
**structure** | **str** | Exported IFC will include the structure from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include structure(NONE) | [optional] [default to 'UPDATED']
**uuids** | **list[str]** | Exported IFC will only have those elements. If omitted, all elements will be exported | [optional] 
**file_name** | **str** | The name of the exported IFC file. It MUST end with .ifc or the exported file won&#39;t be processed by BIMData | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


