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

#get a token
api_instance = swagger_client.AuthenticationApi()
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password
api_response = api_instance.api_system_v1_auth_token_post()
#print(api_response)

#example API call
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.api_key['X-Auth-Token'] = api_response.token
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password

#Start using API calls
api_response = api_instance.api_v2_ippool_get()

#print(api_response)

for pool in api_response['response']:
  print("Found Pool: ", pool['ipPoolName'])
  
  if pool['ipPoolName'] in delete_list:
      print("Deleting Pool with name: ", pool['ipPoolName'])
      api_response = api_instance.api_v2_ippool_pool_id_delete(pool['id'])

