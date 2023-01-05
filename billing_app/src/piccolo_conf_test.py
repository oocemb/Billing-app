from piccolo_conf import *  # noqa

DB = PostgresEngine(
    config={
        "database": os.getenv("DB_NAME", "billing_database"),
        "user": os.getenv("DB_USER", "app"),
        "password": os.getenv("DB_PASSWORD", "123qwe"),
        "host": os.getenv("HOST", "localhost"),
        "port": os.getenv("PORT", 5434),
    }
)
