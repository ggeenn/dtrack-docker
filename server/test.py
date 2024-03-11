import os
import deptrack

dtapi_host = os.environ['DEEPRISK_DTAPI_HOST']
dtapi_token = os.environ['DEEPRISK_DTAPI_TOKEN']
dtapi_vuln_id = os.environ['DEEPRISK_DTAPI_VULN_ID']

dtapi = deptrack.DepTrack(f'http://{dtapi_host}:8080', dtapi_token)
projects = dtapi.get_projects()
for p in projects:
    print(f"{p['name']} was found, id = {p['uuid']}")
