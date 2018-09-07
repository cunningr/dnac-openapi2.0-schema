#!/usr/local/bin/python3

from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
import json

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
api_instance = swagger_client.NetworkDeviceApi()
api_instance.api_client.configuration.api_key['X-Auth-Token'] = api_response.token
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password
#print(dir(api_instance))

#Start using API calls
api_response = api_instance.api_v1_network_device_get()

#print(api_response.response.hostname)

device_dict = api_response.response

for device in device_dict:
  
  if 'POD3-FE-1' in device.hostname:
      print(device.id)
      api_response = api_instance.api_v1_network_device_id_get(device.id)
      print(api_response)
  
