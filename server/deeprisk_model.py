import logging
import re
import urllib.parse

from fastapi import FastAPI, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

class DeepriskModel:
    def __init__(self, uri, name):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.get_database(name)

    def close(self):
        self.db.client.close()

def parse_purl(purl):

    try:
        github = ''
        purl = urllib.parse.unquote(purl)
        if purl.startswith('pkg:golang/'):
            # pkg:golang/github.com/masterminds/squirrel@v1.5.3
            l = re.split('@', purl)
            pkgkey = l[0]
            github = f"https://{pkgkey.replace('pkg:golang/', '')}"
        else:
            #if purl.startswith('pkg:npm/'):
            #if purl.startswith('pkg:deb/'):
            l = re.split('@', purl)
            if len(l) <= 2:
                pkgkey = l[0]
            else:
                pkgkey = f'{l[0]}@{l[1]}'

        return True, pkgkey, github
    except Exception as e:
        logger.error(f"Can't parse {purl}\n Error {e}")
        return False, '', ''
