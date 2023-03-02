#!/usr/bin/env python3

import os
import requests
import random
import time
import sys
import json
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# Pass Azure subscription details 
SUBSCRIPTION_ID = "your_subscription_id"
azure_credential = DefaultAzureCredential()

# Get VM details from Azure
resource_group_name = str(sys.argv[1])
vm_name = str(sys.argv[2])
# printing environment variables
endpoint = os.getenv('IDENTITY_ENDPOINT')+"?resource=https://management.azure.com/"
identityHeader = os.getenv('IDENTITY_HEADER')
payload={}
headers = {
'X-IDENTITY-HEADER' : identityHeader,
'Metadata' : True
}
response = requests.get(endpoint, headers)

# Initialize client with credentials and subscription details
compute_client = ComputeManagementClient(
    azure_credential,
    SUBSCRIPTION_ID
)

# Start Azure VM 
async_vm_start = compute_client.virtual_machines.begin_start(
    resource_group_name, vm_name)
async_vm_start.wait()

# Define how far out to check for appointments
max_days = 365

#Create a function to send emails
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

# Setup links for the API query 
appointment_url = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={}&minimum=1"
login_url = "https://ttp.dhs.gov/"

# Pass details of the locations that should be scanned for appointment availability
location_ids = [5466, 16517]
location_names = ["San Francisco", "Toledo"]

# Run the API query
i = 0
for ids in location_ids:
    url = appointment_url.format(ids)
    appointments = requests.get(url).json()
    if appointments:
        available_date = datetime.strptime(appointments[0]['startTimestamp'], '%Y-%m-%dT%H:%M')
        if available_date <= (datetime.now() + timedelta (days=max_days)):
            print (f"There is a Global Entry appointment available in {location_names[i]} on {available_date.date()} at {available_date.time()}")
            subject = "Global Entry appointment available"
            body = "There is a Global Entry appointment available in {} on {} at {}.\n\n Login now to schedule your appointment - {}".format(location_names[i], available_date.date(), available_date.time(), login_url)
            sender = "sender_email"
            recipients = ["receipient_email_1", "receipient_email_2"]
            password = "your_app_password"
            send_email(subject, body, sender, recipients, password)
    else:
      print (f"No appointments available in {location_names[i]} for the next {max_days} days")
    i += 1
    # Wait 5 sec before the next API ping
    time.sleep(5)

# Stop and deallocate Azure VM
async_vm_stop = compute_client.virtual_machines.begin_deallocate(
    resource_group_name, vm_name)
async_vm_stop.wait()
