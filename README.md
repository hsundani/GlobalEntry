# Global Entry Appointment Availability Checker

This code is a Python script that queries the US Customs and Border Protection (CBP) Trusted Traveler Program (TTP) API to check for available Global Entry appointments at specified locations. If an appointment is available within the next year, the script sends an email and/or text message to alert the user. The script also starts and stops an Azure virtual machine to run the query and conserve local resources.

## Prerequisites
- Python 3
- Azure subscription details and Azure Python SDK installed
- Twilio account details and Twilio Python SDK installed
- Gmail account with app password (or similar email provider) for sending emails

## Installation
- Install Python 3 on your system.
- Install the Azure Python SDK by running the following command in your terminal:
    pip install azure-mgmt-compute
- Install the Twilio Python SDK by running the following command in your terminal:
    pip install twilio
- Clone or download the script to your local system.

## Set the following environment variables:
- IDENTITY_ENDPOINT and IDENTITY_HEADER: These environment variables are required for Azure VM authentication. They should be set to the Identity Endpoint and the Identity Header values provided by your Azure subscription.
- SUBSCRIPTION_ID: The Azure subscription ID that should be used for VM management.
- TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN: These are your Twilio API credentials. You can obtain them by signing up for a Twilio account and creating a new project.
- SENDER_EMAIL, RECIPIENT_EMAIL_1, RECIPIENT_EMAIL_2, and APP_PASSWORD: These are the credentials of your Gmail account. The SENDER_EMAIL variable should be set to the email address of your Gmail account, and the APP_PASSWORD variable should be set to the App Password generated by Gmail for the script.
- In the global_entry_checker.py file, set the resource_group_name and vm_name variables to the name of the Azure resource group and virtual machine that you want to use for running the script.
- In the same file, set the location_ids and location_names variables to the IDs and names of the locations that you want to check for appointment availability.

## Usage
- Open a terminal and navigate to the directory containing the script.
- Run the following command to execute the script with the required arguments:
    - python3 global_entry_checker.py <resource_group_name> <vm_name>
- Replace <resource_group_name> with the name of the resource group where the Azure VM is located and <vm_name> with the name of the Azure VM.
    - For example: python3 global_entry_checker.py myResourceGroup myVM
- The script will start an Azure virtual machine and begin querying the TTP API for available appointments at the specified locations.
- If an appointment is found within the next year, the script will send an email and/or text message to alert the user.
- Once the query is complete, the script will stop and deallocate the Azure VM.

## Code Walkthrough
- Import required libraries:
  - os - provides a way of interacting with the operating system
  - requests - allows the script to send HTTP requests
  - random - generates random numbers
  - time - provides time-related functions
  - sys - provides access to some variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter.
  - json - allows the script to work with JSON-formatted data
  - smtplib - provides a way to send email messages
  - datetime and timedelta - provide functions for working with dates and times
  - DefaultAzureCredential - allows the script to authenticate to Azure using environment variables, managed identities, or service principal credentials
  - ComputeManagementClient - allows the script to manage Azure virtual machines
  - Client - allows the script to send text messages using the Twilio API
- Start the Azure VM using the ComputeManagementClient.
- Define a function to send emails using the smtplib library.
- Define the TTP API query URLs and the location IDs and names to check for availability.
- Run the API query for each location and check if any appointments are available within the next year.
- If an appointment is found, send an email and/or text message to alert the user using the send_email() function and the Client() function from the twilio library.
- Stop and deallocate the Azure VM using the ComputeManagementClient.

## Limitations
- The script can only check for appointment availability at specific locations that are supported by the CBP API. Currently, the script is set up to check for availability at San Francisco and Toledo locations, but this can be easily modified by changing the location_ids and location_names variables.
- The script can only check for appointment availability within a specified time range (365 days by default). This can be modified by changing the max_days variable.
- The script relies on external services (Azure, Twilio, Gmail) for authentication and notification, so it may incur additional costs or require additional setup.
