import os
import deptrack

dtapi_host = 'dependency-track.oak.in.ua'#os.environ['DEEPRISK_DTAPI_HOST']
dtapi_token = 'JZfG1TiVaXIrmikDNTcutSU3QAtb5rhz'#os.environ['DEEPRISK_DTAPI_TOKEN']

dtapi = deptrack.DepTrack(f'http://{dtapi_host}:8000', dtapi_token)
projects = dtapi.get_projects()
for p in projects:
    print(f"{p['name']} was found, id = {p['uuid']}")
