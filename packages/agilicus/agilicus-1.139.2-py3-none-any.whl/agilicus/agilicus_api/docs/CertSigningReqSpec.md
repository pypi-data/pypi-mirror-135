# CertSigningReqSpec

The specification for the CertSigningReq

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_id** | **str** | Unique identifier | 
**request** | **str** | The certificate signing request (CSR) formatted as PEM.  | 
**auto_renew** | **bool** | When enabled (true), system will automatically renew the certificate using the provided request CSR.  The resulting certificate will be updated in CertSigningReqCertificateStatus.  | [optional]  if omitted the server will use the default value of True
**rotate_keys** | **bool** | Provided as a mechansim to notify a user/client to rotate their keys. A client would retrieve this and the client would then issue a new request. A subsequent PUT with a new request will reset this property to false. This may be true whereby a user has decided to update all keys, and this facility could be made available via the administration portal.  | [optional] 
**private_key_id** | **str** | The associated private key id that created the CSR request.  A private key id is defined as the md5 sum of private keys&#39; public key.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


