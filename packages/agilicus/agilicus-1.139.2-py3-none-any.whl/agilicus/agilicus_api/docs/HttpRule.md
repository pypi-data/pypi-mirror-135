# HttpRule

A rule condition applied to the attributes of an http request.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rule_type** | **str** | Used to distinguish between different types of rule | defaults to "HttpRule"
**methods** | **[str]** | The HTTP methods to allow. If any of the listed methods are matched, then this portion of the rule matches.  | [optional] 
**path_regex** | **str** | regex for HTTP path. Can be templatized with jinja2 using definitions collection. | [optional] 
**path_template** | [**TemplatePath**](TemplatePath.md) |  | [optional] 
**query_parameters** | [**[RuleQueryParameter]**](RuleQueryParameter.md) | A set of constraints on the parameters specified in the query string. | [optional] 
**body** | [**RuleQueryBody**](RuleQueryBody.md) |  | [optional] 
**matchers** | [**RuleMatcherList**](RuleMatcherList.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


