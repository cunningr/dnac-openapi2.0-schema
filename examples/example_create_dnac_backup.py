#!/usr/local/bin/python3

from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

host = "https://127.0.0.1:8888"
username = 'admin'
password = 'admin'

delete_list = ['test_200', 'test_201', 'test_202', 'test_203', 'test_204', 'test_205']

# get a token
api_instance = swagger_client.AuthenticationApi()
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password
api_response = api_instance.api_system_v1_auth_token_post()
# print(api_response)

# Configure API client
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.api_key['X-Auth-Token'] = api_response.token
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password

# Start using API calls
api_response = api_instance.api_system_v1_maglev_backup_get()

#print(api_response.response)

# Create an object for a new backup
#backup = swagger_client.Backup(description='cunningr-test')
#api_response = api_instance.api_system_v1_maglev_backup_post(backup)

# Restore a given backup point
#targetBackup = "Pod1-Base"
#api_response = api_instance.api_system_v1_maglev_backup_get()
#for backupPoint in api_response.response:
#    if targetBackup in backupPoint['description']:
#        api_response = api_instance.api_system_v1_maglev_restore_backup_id_post(backupPoint['backup_id'])


#print(api_response.response)

# Delete a backup from list of existing backup points
#targetBackup = "cunningr-test"
#api_response = api_instance.api_system_v1_maglev_backup_get()
#for backupPoint in api_response.response:
#    if targetBackup in backupPoint['description']:
#        api_response = api_instance.api_system_v1_maglev_backup_backup_id_delete(backupPoint['backup_id'])

api_response = api_instance.api_system_v1_maglev_backup_progress_get()
print(api_response)


