# Unit

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] [readonly] 
**type** | **str** | IfcDerivedUnit, IfcContextDependentUnit, IfcConversionBasedUnit, IfcSIUnit or IfcMonetaryUnit | 
**name** | **str** | Name of the unit (ex: DEGREE) | [optional] 
**unit_type** | **str** | IFC type of the unit or user defined type (ex: PLANEANGLEUNIT for DEGREE and RADIAN) | [optional] 
**prefix** | **str** | Litteral prefix for scale (ex: MILLI, KILO, etc..) | [optional] 
**dimensions** | **list[float]** | List of 7 units dimensions | [optional] 
**conversion_factor** | **float** | Factor of conversion and base unit id (ex: DEGREE from RADIAN with factor 0.0174532925199433) | [optional] 
**conversion_baseunit** | [**Unit**](Unit.md) |  | [optional] 
**elements** | [**object**](.md) | List of constitutive unit elements by id with corresponding exponent (ex: [meterID/1, secondID/-1] for velocity) | [optional] 
**is_default** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


