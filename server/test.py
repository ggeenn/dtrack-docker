import os
import deptrack
import deeprisk_model

#dtapi_host = 'https://dependency-track.oak.in.ua'#os.environ['DEEPRISK_DTAPI_HOST']
#dtapi_token = 'JZfG1TiVaXIrmikDNTcutSU3QAtb5rhz'#os.environ['DEEPRISK_DTAPI_TOKEN']
#
#dtapi = deptrack.DepTrack(f'{dtapi_host}', dtapi_token)
#projects = dtapi.get_projects()
#for p in projects:
#    print(f"{p['name']} was found, id = {p['uuid']}")

#u = 'pkg:golang/git.oak.in.ua/volia/zahyst-go-common@v0.0.0-20240117152438-4c093fcda720'
#u = 'pkg:npm/abab@1.0.4'
#u = 'pkg:deb/acl@2.3.1?arch=amd64&distro=debian-12&distro_name=bookworm'
u = 'pkg:deb/ubuntu/bsdutils@1:2.34-0.1ubuntu9.4?arch=amd64&distro=ubuntu-20.04&upstream=util-linux'
print(deeprisk_model.parse_purl(u))
