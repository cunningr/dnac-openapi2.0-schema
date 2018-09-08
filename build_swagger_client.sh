#!/bin/bash

python3 getDnacOpenAPISchema.py
swagger-codegen generate -i ./dnac1.2_swagger.yml -l python -o ~/dnac-api-client -D packageName=dnac_api_client

