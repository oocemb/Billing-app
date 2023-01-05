import os
import sys


from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError, errorcodes, errors, InterfaceError

from setup_logging import *

logger = get_logger()

# load_dotenv()


class PGAdapter:
    __instance = None
    connection = None

    def __init__(self):
        if not PGAdapter.__instance:
            self.get_connection()

        else:
            logger.info("Connection to PG DataBase already created")
            pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = PGAdapter()
        return cls.__instance

    @classmethod
    def get_connection(cls):
        dsl = {
            "dbname": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
            "host": os.environ.get("DB_HOST", "127.0.0.1"),
            "port": os.environ.get("DB_PORT", 5432),
        }
        try:
            cls.connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)

        except OperationalError as err:
            # set the connection to 'None' in case of error
            pass

        return cls.connection
