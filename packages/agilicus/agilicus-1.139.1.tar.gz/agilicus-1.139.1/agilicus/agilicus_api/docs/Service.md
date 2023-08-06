# Service

A Service defines a multitenant application which is operated by Agilicus. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Service name. Must be unique accross all Applications and Services. | 
**org_id** | **str** | organisation id | 
**base_url** | **str** | The URL which forms the base of this service. This value will be joined with the paths in the rules for this service to form its authorization model.  | 
**created** | **datetime** | Creation time | [optional] [readonly] 
**id** | **str** | Unique identifier | [optional] [readonly] 
**description** | **str** | Service description text | [optional] 
**contact_email** | **str** | Administrator contact email | [optional] 
**roles** | [**RoleList**](RoleList.md) |  | [optional] 
**definitions** | [**[Definition]**](Definition.md) | List of definitions | [optional] 
**updated** | **datetime** | Update time | [optional] [readonly] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


