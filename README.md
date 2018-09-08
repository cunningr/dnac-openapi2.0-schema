The OpenAPI2.0 schema is built on top of the schema published by Cisco's Devnet [here](https://pubhub.devnetcloud.com/media/dna-center-api-1-2/docs/swagger_apis_06052018.json)

The ```dnac1.2_swagger_custom.yml``` is used to add new path and model definitions that are not currently included in the published schema.  The two two schema are merged and then the python package ```dnac-api-client``` is built using ```swagger_codegen``` (see build_swagger_client.sh)

Note: During the merge, we also add a security definition and modify the path ```/api/system/v1/auth/token``` to use the ```basic`` method.  This makes getting a token using the `danc_api_client``` package a little easier (see examples).

The resulting python package is maintained on github [here](https://github.com/cunningr/dnac-api-client).

Please feel free to fork this project and make a pull request for any updates or modifications to the ```dnac1.2_swagger_custom.yml``` so that they can be included in ```dnac-api-client``` package.
