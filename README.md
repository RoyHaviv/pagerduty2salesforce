# pagerduty2salesforce

## Description

This is a project that allows pagerduty to open cases in Salesforce.

Use will only be made if there is an alert on Pager Duty which needs escalation to support.

### Requirements

+ You need to create an integration key on PagerDuty and add it to environment variables. 
+ add the following environment variables.

```
$env:PDKEY=<Get the key from your PagerDuty admin>
$env:SF_SESSION_USERNAME=product.integration@checkmarx.com
$env:SF_SESSION_PASSWORD=<Get the password from AWS Secrets Manager>
$env:SF_SESSION_SECURITY_TOKEN=<Get the token from AWS Secrets Manager>
$env:SF_SESSION_DOMAIN=login
```
