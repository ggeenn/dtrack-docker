import os
import logging
import re

from fastapi import FastAPI, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

import deeprisk_model
import deptrack
import githist

mongo_user = os.environ['DEEPRISK_MONGO_USER']
mongo_password = os.environ['DEEPRISK_MONGO_PASS']
mongo_host = os.environ['DEEPRISK_MONGO_HOST']
mongo_port = '27017'
mongo_db_name = 'deepriskdb'

# MongoDB URI including authentication credentials
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
db = None
dtapi = None

dtapi_host = os.environ['DEEPRISK_DTAPI_HOST']
dtapi_token = os.environ['DEEPRISK_DTAPI_TOKEN']
dtapi_vuln_id = os.environ['DEEPRISK_DTAPI_VULN_ID']

@app.on_event("startup")
async def startup_db_client():
    global db
    client = AsyncIOMotorClient(mongo_uri)
    db = client.get_database(mongo_db_name)
    dtstatus = ''
    global dtapi
    try:
        dtapi = deptrack.DepTrack(f'http://{dtapi_host}:8080', dtapi_token)
        projects = dtapi.get_projects()
        dtstatus = f'found {len(projects)} projects'
    except Exception as e:
        dtstatus = f'Error: {e}'
    
    logger.info(f'Dependancy Track on {dtapi_host}: {dtstatus}')

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()

@app.get("/")
async def read_root():
    logger.info("Root endpoint was called")
    return {"Hello": "World"}

@app.get("/scan")
async def start_scan():
    repos = set()
    packages = set()
    logger.info("Scanning is in progress...")
    projects = dtapi.get_projects()
    for p in projects:
        logger.info(f"{p['name']} was found, id = {p['uuid']}")
        components = dtapi.get_components_by_project_uuid(p['uuid'])
        logger.info(f'{len(components)} were found,')
        for c in components:
            if 'purl' in c:
                purl = c['purl']
                ptype, pname, psubname, pver, _ = re.split(r'[?@/]', purl)
                pkgkey = f'{ptype}/{pname}/{psubname}'
                repos.add(pkgkey)
                packages.add(purl)

    repos_db = db["repos"]
    count = len(repos)
    for p in repos:
        repo = await repos_db.find_one({"pkgkey": p})
        if not repo:
            logger.info(f'New repo inserted : {p}')
            await repos_db.insert_one({'pkgkey':p, 'github':''})
        else:
            url = repo['github']
            if len(url) != 0:
                count -= 1

    packages_db = db["packages"]
    for purl in packages:
        package = await packages_db.find_one({"purl": purl})
        if not package:
            logger.info(f'New package inserted : {purl}')
            ptype, pname, psubname, pver, _ = re.split(r'[?@/]', purl)
            pkgkey = f'{ptype}/{pname}/{psubname}'
            await packages_db.insert_one({'purl':purl, 'pkgkey':pkgkey, 'github':'', 'contributors':[]})

    logger.info(f'{count} repos should be filled')
    return {'Repos should be filled':count}

@app.get("/populate")
async def populate():
    packages_db = db["packages"]
    pipeline = [
        {
            "$lookup": {
                "from": "repos",  # The collection to join
                "localField": "pkgkey",  # The field from the 'packages' collection
                "foreignField": "pkgkey",  # The field from the 'repos' collection to match on
                "as": "repo_info"  # The array field to add to the input documents; contains the matching documents from 'repos'
            }
        },
            {
        "$match": {"repo_info": {"$ne": []}}
    }
    ]
    async for m in packages_db.aggregate(pipeline):        
        for r in m['repo_info']:
            if len(r['github']) > 0:
                logger.info(f'Filled github Found for {r["pkgkey"]} : {r["github"]}')
                await packages_db.update_many({"pkgkey": r["pkgkey"]},
                                              {"$set": {"github": r["github"]}})

    contributors_db = db["contributors"]

    query = {"github": {"$exists": True, "$ne": ""}}

    count = 0
    cursor = packages_db.find(query)
    async for d in cursor:
        if 'populated' in d and d['populated']:
            continue
        await packages_db.update_one({"_id": d["_id"]},
                                     {"$set": {"populated": True}})
        logger.info(f'Filled github Found for {d}')
        github = d['github']
        try:
            contributors = githist.collect(github, '1900-01-01')
        except Exception as e:
            logger.error(f'Error {e}')

        for c in contributors:
            ivan = await contributors_db.find_one({'name': c['name']})
            if not ivan:
                logger.info(f'New ivan found : {c}')
                count += 1
                await contributors_db.insert_one(c | {'github':github})

    return {'New contributors found': count}

@app.get("/upload_score")
async def upload_score():
    packages_db = db["packages"]
    query = {"score": {"$exists": True, "$ne": 0}}
    cursor = packages_db.find(query)
    count = 0
    async for d in cursor:
        logger.info(f'Found scored package {d}')
        dtapi.assign_vuln_by_purl(d['purl'], dtapi_vuln_id)
        count += 1

    return {'Packages uploaded': count}