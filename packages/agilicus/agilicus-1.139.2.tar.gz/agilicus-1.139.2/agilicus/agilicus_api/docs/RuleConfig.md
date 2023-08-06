# RuleConfig

A Rule defines a set of conditions which, if matched, allow a request to proceed through the system. If no rules match, the request will be denied. The Rule is a base class, with more concrete classes specifying precise match conditions. Rules may be associated with roles to allow for users to be granted collections of rules. Rules are uniquely identified by their id. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the rule. | 
**roles** | **[str]** | The list of roles assigned to this rule. | [optional] 
**excluded_roles** | **[str]** | The list of roles assigned to this rule. | [optional] 
**comments** | **str** | A description of the rule. The comments have no functional effect, but can help to clarify the purpose of a rule when the name is not sufficient.  | [optional] 
**condition** | [**HttpRule**](HttpRule.md) |  | [optional] 
**scope** | [**RuleScopeEnum**](RuleScopeEnum.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


