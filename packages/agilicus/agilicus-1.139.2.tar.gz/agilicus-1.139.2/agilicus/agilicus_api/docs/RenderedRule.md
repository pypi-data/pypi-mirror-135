# RenderedRule

Rendered rule

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**methods** | **[str]** | The HTTP method to allow. | [optional] 
**paths** | **[str]** | regex for HTTP path. | [optional] 
**template_paths** | [**[TemplatePath]**](TemplatePath.md) | A list of template paths to match against. The first match in the list will be used. Be careful if they overlap: put more precise paths first in the list. A template can be used to provide information for more precise matchers as configured by http_extractors.  | [optional] 
**query_parameters** | [**[RenderedQueryParameter]**](RenderedQueryParameter.md) | A set of constraints on the parameters contained in the query string. | [optional] 
**body** | [**RenderedRuleBody**](RenderedRuleBody.md) |  | [optional] 
**resource_info** | [**ResourceInfo**](ResourceInfo.md) |  | [optional] 
**matchers** | [**RuleMatcherList**](RuleMatcherList.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


