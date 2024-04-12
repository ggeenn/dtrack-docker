import json
import os
import sys

def translateBom(fname):
    f = open(fname)
    data = json.load(f)
    componentns = data['components']
    with open(f'{fname}.txt', 'w') as out:
        for c in componentns:
            purl = c.get('purl', None)
            if not purl:
                continue
            exts = c.get('externalReferences', [])
            url = ''
            for e in exts:
                url = e.get('url', '')
                if e.get('type', '') == 'vcs':
                    break
            print(f'{purl};{url}', file=out)

def main():
    if len(sys.argv) != 2:
        print(f'usage: \n> {sys.argv[0]} <bomfile.json>')
        exit()
    translateBom(sys.argv[1])

main()