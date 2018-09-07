# OpenAPI

## DNAC

Was able to download OpenAPI.json spec for swagger2.0 via Devnet using the developer tools in chrome.  The link found was [this one](https://pubhub.devnetcloud.com/media/dna-center-api-1-2/docs/swagger_apis_06052018.json)

Copy/paste this into the [swagger editor](https://editor.swagger.io) console to convert it to YAML and fix a few issues;

 - The ```licenseUrl``` and ```termsOfServiceUrl``` throw an error but we can ignore as this is just metadata

```
  licenseUrl: 'https://developer.cisco.com'
  termsOfServiceUrl: 'http://www.cisco.com/web/siteassets/legal/terms_condition.html'
...
  license: Cisco DevNet
```

 Added API version, but this also seems not entirely necessary;

```
  version: "1.0.0"
```

Finally we need to add ```securityDefinitions``` and ```security``` to tell the client to add the auth token to the header of every request.  Also add ```basicAuth``` so we may set this for the ```/api/system/v1/auth/token``` API.

```
securityDefinitions:
  basicAuth:
    type: basic
  APIKeyHeader:
    type: apiKey
    in: header
    name: X-Auth-Token
```

Set ```APIKeyHeader``` as the default auth.

```
security:
  - APIKeyHeader: []
```

The editor throws a couple more minor errors but we can ignore for now.

Select all and copy/paste to a text file locally then used the following to generate client code;

```swagger-codegen generate -i ./dnac1.2-swagger.yml -l python -o ./dnac1.2```

Once the client is generated, we need to manually update the ```ssl_verify``` option to ```False``` if we want to use self-signed (there should be a way to override this in the python script - but so far no luck).

 - Update ```swagger_client/configuration.py``` to certificate ```ssl_verify = False```.

Get a token like this ...

```
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.host = "https://10.62.6.100"
request = swagger_client.GenerateTokenRequest()
authorization = 'Basic <Base64_encoded 'username:password' string>'
api_response = api_instance.api_system_v1_auth_token_post(request, authorization)

```

Actually, it should not necessary to send any body (```request = swagger_client.GenerateTokenRequest()```) however this is defined in the API spec, so without it you will get an error for missing param.  If you want to update the spec and remove this, search for the ```/api/system/v1/auth/token``` definition and remove the ```request``` definition:

```
        - name: request
          description: request
          required: true
          schema:
            $ref: '#/definitions/GenerateTokenRequest'
          in: body
```

Regenerate the client code from the updated schema and you should be able to simply do:

```
# create an instance of the API class
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.host = "https://10.62.6.100"
authorization = 'Basic <Base64_encoded 'username:password' string>'
api_response = api_instance.api_system_v1_auth_token_post(authorization)
```

It is possible to update the ```/api/system/v1/auth/token``` definition to use ```basicAuth```.  This will allow us to set the username and password in the client config and have the client automatically generate the required base64 string.  Also since then the ```authorization``` option is not required to be passed, we can remove this also from the spec:

```
  /api/system/v1/auth/token:
    post:
      operationId: ''
      tags: []
      summary: Generate Token
      description: This method is used to generate token.
+      security:
+        - basicAuth: []
      consumes:
        - application/json
      produces:
        - application/json
-      parameters:
-        - name: request
-          description: request
-          required: true
-          schema:
-            $ref: '#/definitions/GenerateTokenRequest'
-          in: body
-        - name: Authorization
-          description: '<username:password> of 64 based encoded string'
-          default: Basic YWRtaW46TWFnbGV2MTIz
-          required: true
-          type: string
-          in: header
      responses:
        '200':
          description: successful token generation
          schema:
            $ref: '#/definitions/GenerateTokenResponse'
        '401':
          description: invalid credentials.
```

```
from __future__ import print_function
import base64
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

host = "https://dnac-ip"
username = '<USERNAME>'
password = '<PASSWORD>'
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password
api_response = api_instance.api_system_v1_auth_token_post()
```

With the above hacks to the schema in place, here is complete example:

```
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

host = "https://dnac-ip"
username = '<USERNAME>'
password = '<PASSWORD>'
    
#get a token
api_instance = swagger_client.DefaultApi()
api_instance.api_client.configuration.host = host
api_instance.api_client.configuration.username = username
api_instance.api_client.configuration.password = password
api_response = api_instance.api_system_v1_auth_token_post()

#example API call
api_instance.api_client.configuration.api_key['X-Auth-Token'] = api_response.token
api_response = api_instance.api_v1_topology_site_topology_get()

print(api_response)

ipPool = swagger_client.models.ippool.Ippool(gateways=['10.0.0.1'], ip_pool_cidr='10.0.0.0/24', ip_pool_name='new_pool')
api_response = api_instance.api_v2_ippool_post(ipPool)

api_response = api_instance.api_v2_ippool_get()
for i in api_response['response']:
    print(i['ipPoolName'] + " : " + i['id'])

#Need to grab the ID for the pool you want to delete
#api_response = api_instance.api_v2_ippool_pool_id_delete('53efcb85-3276-435a-8770-00ad8639203f')

```

## ToDo

