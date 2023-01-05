import os
import sys
import requests
import json
import pathlib

from setup_logging import *
from dotenv import load_dotenv


load_dotenv()
logger = get_logger()

HOST = os.environ.get("ES_HOST", "127.0.0.1")
PORT = os.environ.get("ES_PORT", 9200)
ES_URL = f"http://{str(HOST)}:{PORT}/movies"

headers = {
    "Content-type": "application/x-ndjson",
}

json_name = pathlib.Path(sys.argv[0]).parent / pathlib.Path(
    "init/movies_es_schema.json"
)
f = open(json_name)
query = json.load(f)
response = requests.put(ES_URL, headers=headers, data=query)

logger.info("Elasticsearch initialisation results")
logger.info(response.content)
