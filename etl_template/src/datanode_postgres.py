import os
import sys

import backoff
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError, errorcodes, errors, InterfaceError, DatabaseError

from datanode import DataNode
from pg_adapter import *
from setup_logging import *

logger = get_logger()
load_dotenv()


class DataNodePostgres(DataNode):
    def __init__(self):
        self.connection = None
        self.connect()

    def backoff_hdlr(details):
        logger.warning(
            "PG Connect  - Backing off {wait:0.1f} seconds after {tries} tries ".format(
                **details
            )
        )

    @backoff.on_exception(
        backoff.expo, (OperationalError, InterfaceError), on_backoff=backoff_hdlr
    )
    def connect(self):
        conn = PGAdapter.get_instance()
        self.connection = conn.get_connection()

    def pull(self, sqlquery):
        try:
            if self.connection is None:
                self.connect()

            cur = self.connection.cursor()
            cur.execute(sqlquery)
            batch_size = int(os.environ.get("BATCH_SIZE"))
            results = cur.fetchmany(batch_size)
            return results

        except OperationalError as err:
            self.connect()
            raise ValueError

        except InterfaceError as err:
            self.connect()
            raise ValueError

        except Exception as err:
            self.connect()
            raise ValueError

    def push(self, data):
        pass
