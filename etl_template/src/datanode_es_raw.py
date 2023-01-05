from datanode import DataNode
import os
import sys
import requests
import json
import backoff
from dotenv import load_dotenv

from setup_logging import *

logger = get_logger()
load_dotenv()


class DataNodeES(DataNode):
    def __init__(self):
        (self.HOST, *args) = (os.environ.get("ES_HOST", "127.0.0.1"),)
        self.PORT = os.environ.get("ES_PORT", 9200)
        self.ES_SERVER = f"http://{str(self.HOST)}:{self.PORT}/"

    def connect(self):
        pass

    def push(self, data):
        self.push_bulk(data)

    def pull(self, query):
        pass

    def push_single(self, data):
        headers = {
            "Content-type": "application/x-ndjson",
        }

        for odd in data:
            odd_json = json.dumps(odd)
            query_string = odd_json
            logger.info(odd_json)

            response = requests.post(
                f"{self.ES_SERVER}/movies/_doc/", headers=headers, data=query_string
            )
            logger.info(response.text)

    def push_bulk(self, data):
        if len(data) > 0:
            logger.info("RUN DataNodeES -push bulk")
            bulk_query = ""
            for odd in data:
                even_json = (
                    '{"index": {"_index": "movies", "_id": "' + odd["id"] + '"}}\n'
                )
                odd_json = json.dumps(odd)
                bulk_query = bulk_query + even_json + odd_json + "\n"

            headers = {
                "Content-type": "application/x-ndjson",
            }

            response = self.es_post_query(
                f"{self.ES_SERVER}/_bulk", headers=headers, data=bulk_query
            )
            logger.info(response.text)

            return response
        else:
            logger.info("SKIP DataNodeES - no data")
            return

    def backoff_hdlr(details):
        logger.warning(
            "Elasticsearch - Backing off {wait:0.1f} seconds after {tries} tries ".format(
                **details
            )
        )

    @backoff.on_exception(
        backoff.expo,
        (requests.HTTPError, requests.ConnectionError),
        on_backoff=backoff_hdlr,
    )
    def es_post_query(self, url, headers, data):
        response = requests.post(url, headers=headers, data=data)
        return response
