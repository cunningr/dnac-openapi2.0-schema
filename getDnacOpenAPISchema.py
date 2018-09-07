#!/usr/local/bin/python3

import requests
import yaml
import json

schemaUrl = "https://pubhub.devnetcloud.com/media/dna-center-api-1-2/docs/swagger_apis_06052018.json"

r = requests.get(schemaUrl)

schemaDict = r.json()

ymlSecurityDefinitions = """
securityDefinitions:
  basicAuth:
    type: basic
  APIKeyHeader:
    type: apiKey
    in: header
    name: X-Auth-Token
"""

ymlApiSecurity = """
security:
  - APIKeyHeader: []
"""

ymlBasicSecurity = """
security:
  - basicAuth: []
"""

securityDefinitions = yaml.load(ymlSecurityDefinitions)
apiSecurity = yaml.load(ymlApiSecurity)
basicSecurity = yaml.load(ymlBasicSecurity)

#Add security definitions and set default security
schemaDict.update(securityDefinitions)
schemaDict.update(apiSecurity)

#Hack /api/system/v1/auth/token
schemaDict['paths']['/api/system/v1/auth/token']['post'].pop('parameters', None)
schemaDict['paths']['/api/system/v1/auth/token']['post'].update(basicSecurity)

#Add custom definitions
with open("dnac1.2_swagger_custom.yml", 'r') as stream:
    customSchemaDict = yaml.load(stream)

for key, path in customSchemaDict['paths'].items():
    schemaDict['paths'].update({key : path})

for key, definition in customSchemaDict['definitions'].items():
    schemaDict['definitions'].update({key : definition})

with open('dnac1.2_swagger.yml', 'w') as outfile:
    yaml.safe_dump(schemaDict, stream=outfile, default_flow_style=False)
