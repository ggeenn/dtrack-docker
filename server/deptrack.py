import requests
import json

def json2file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

class DepTrack:
    def __init__(self, url, api_key):
        self.base_url = f'{url}/api/v1'
        self.headers = {'X-Api-Key': api_key}

    def get_json(self, path, params=None):
        url = f'{self.base_url}/{path}'
        r = requests.get(url, params=params, headers=self.headers)
        if r.status_code != 200:
            raise RuntimeError(f'{url} failed : {r.status_code}')
        return r.json()
    
    def post_json(self, path):
        url = f'{self.base_url}/{path}'
        r = requests.post(url, headers=self.headers)
        if r.status_code != 200:
            raise RuntimeError(f'{url} failed : {r.status_code}')
    
    def get_projects(self):
        return self.get_json('project')
    
    def get_project_by_name(self, project_name):
        projects = self.get_projects()
        for p in projects:
            if p['name'] == project_name:
                return p
        return None
    
    def get_components_by_project_uuid(self, uuid):
        return self.get_json(f'component/project/{uuid}')
    
    def get_vuln_by_name(self, name):
        vulns = self.get_json('vulnerability')
        for v in vulns:
            if v['vulnId'] == name:
                return v
        return None
    
    def assign_vuln_by_purl(self, purl, vuln_id):
        components = self.get_json('component/identity', {'purl':purl})
        if not components or len(components) < 1:
            return
        c = components[0]
        self.post_json(f'vulnerability/{vuln_id}/component/{c["uuid"]}')