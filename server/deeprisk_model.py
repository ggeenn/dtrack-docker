import logging
import re

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
        if '?' in purl:
            ptype, pname, psubname, pver, _ = re.split(r'[?@/]', purl)
        else:
            ptype, pname, psubname, pver = re.split(r'[@/]', purl)
        return True, ptype, pname, psubname, pver
    except Exception as e:
        logger.error(f"Can't parse {purl}\n Error {e}")
        return False, '', '', '', ''
