import os
import json
from pdpyras import APISession
from simple_salesforce import Salesforce, SalesforceLogin, SFType

def lambda_handler(event, context):
    
    print(event)
    headers = event['headers']
    
    # not needed anymore since we are using the x-api-key on apigateway
    #if 'APIKEY' not in headers.keys() or headers['APIKEY'] != os.getenv('PAGERDUTYAPI'):
    #
    #    return {
    #        'statusCode': 403,
    #        'body': 'Access Denied'
    #    }
    
    body = event['body']

    action_name, action_level = body['messages'][0]['webhook']['name'].split("-")
    #priority = 'High' if body['messages'][0]['webhook']['name'] == 'TicketOnSf-HIGH' else "Normal"
    incident_id = body['messages'][0]['incident']['id']
    summary = body['messages'][0]['log_entries'][0]['incident']['summary']


    # prepare session for sf
    username = os.getenv('SF_SESSION_USERNAME')
    password = os.getenv('SF_SESSION_PASSWORD')
    security_token = os.getenv('SF_SESSION_SECURITY_TOKEN')
    domain = os.getenv('SF_SESSION_DOMAIN')

    #PD API session
    pdkey = os.getenv("PDKEY")
    session = APISession(pdkey)

    #get the incident
    incident_alert_url = f'incidents/{incident_id}/alerts'
    print(f"incident_alert_url={incident_alert_url}")
    incident_alert = session.rget(incident_alert_url)
    print(f"incident_alert={incident_alert}")
    incident_notes_url = f'incidents/{incident_id}/notes'
    print(f"incident_notes_url={incident_notes_url}")
    incident_notes = session.rget(incident_notes_url)
    print(f"incident_notes={incident_notes}")

    sf_name = incident_alert[0]['body']['details']['SFNAME']
    
    content = ""
    if len(incident_notes):
        #print(f"incident_notes={incident_notes}")
        #print(type(incident_notes))
        for note in incident_notes:
            content = content + note['content'] + "\n"
    
    #print(f"incident_id={incident_id}")
    #print(f"summary={summary}")
    #print(f"sf_name={sf_name}")
    #print(f"content={content}")
    
    #Creating a session in salesforce
    session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
    sf = Salesforce(instance=instance, session_id=session_id)

    #SOQL to get the customer account id and write it to json file 
    query = f"SELECT Id FROM Account WHERE Name = '{sf_name}'"
    Account_id = sf.query(query)
    Account = Account_id['records'][0]['Id']

    #Creating the case
    sf.Case.create({'RecordTypeId':'0123z000000VG2yAAG','AccountId':Account,\
        'ContactId':'0034K000007AXhAQAW','Version__c':'******','Hotfix__c':'******',\
            'Product_area__c':'General','Subject':summary,'Description':content,'Origin':'PagerDuty_Integration',\
                'Priority':action_level})
    
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': 'OK'
    }
