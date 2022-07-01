import os
import json
from pdpyras import APISession
from simple_salesforce import Salesforce, SalesforceLogin, SFType


"""
This script runs two API calls.
Fist call access data for a specific resources (Incidents including nots and alert) from a REST API on PagerDuty.
With the data, the script will create a case on Salesforce.
"""
#PD API session
pdkey = os.getenv("PDKEY")
session = APISession(pdkey)

#get the incident
incident_alert = session.rget('incidents/PMUHCC6/alerts')
incident_notes = session.rget('incidents/PMUHCC6/notes')
incident = session.rget('incidents/PMUHCC6')

#Extract PD incident, nots and alert to a Json files
with open("alert_output.json", "w") as json_file:
    json.dump(incident_alert, json_file)

with open("notes_output.json", "w") as json_file:
    json.dump(incident_notes, json_file)

with open("incident_output.json", "w") as json_file:
    json.dump(incident, json_file)




# read the credentials for SF login 
with open("login_CxSession.json", "r") as json_file:
    g = json.load(json_file)

username = g['username']
password = g['password']
security_token = g['security_token']
domain = g['domain']

# read PD alert_output json file
with open ('alert_output.json', 'r') as json_file:
    data_alert = json.loads(json_file.read())
    SF_name = data_alert[0]['body']['details']['SFNAME']
    
# Read the incident from PagerDuty
with open ('incident_output.json', 'r') as json_file:
    data_incident = json.load(json_file)
    summary = data_incident["summary"]

# read the notes_output json file
with open ('notes_output.json', 'r') as json_file:
    data_note = json.loads(json_file.read())
    content = data_note[0]['content']
exit()
#Creating a session in salesforce
session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
sf = Salesforce(instance=instance, session_id=session_id)


#SOQL to get the customer account id and write it to json file 
query = f"SELECT Id FROM Account WHERE Name = '{SF_name}'"
Account_id = sf.query(query)
with open("Accountid.json", "w") as json_file:
    json.dump(Account_id, json_file)

# Read from the account.json 
with open("Accountid.json", "r") as json_file:
    read_id = json.loads(json_file.read())
    Account = read_id['records'][0]['Id']

#Creating the case
sf.Case.create({'RecordTypeId':'0123z000000VG2yAAG','AccountId':Account,\
    'ContactId':'0034K000007AXhAQAW','Version__c':'******','Hotfix__c':'******',\
        'Product_area__c':'General','Subject':summary,'Description':content,'Origin':'PagerDuty_Integration',\
            'Priority':'High','SuppliedEmail':'roy.haviv@checkmarx.com'})



os.remove("alert_output.json")
os.remove("notes_output.json")
os.remove("incident_output.json")
os.remove("Accountid.json")
