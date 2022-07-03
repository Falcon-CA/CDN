import os

import dotenv
from mysql.connector import MySQLConnection, connect

from cdn_global import cdn


def load_environ():
    dotenv.load_dotenv()
    environs = [
        "DB_HOST",
        "DB_NAME",
        "DB_USER",
        "DB_PASS",
        "FILE_PATH"
    ]
    for var in environs:
        assert var in os.environ


def get_connection():
    return connect(
        host=os.environ["DB_HOST"], database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"], password=os.environ["DB_PASS"]
    )


def create_tables(db: MySQLConnection):
    c = db.cursor()
    with open("fca_cdn/tables.sql") as sql_f:
        queries = sql_f.read()
        for query in queries.split(";"):
            c.execute(query)
    db.commit()


def load_indexes(db: MySQLConnection):
    c = db.cursor()
    cdn.file_path = os.environ["FILE_PATH"]

    c.execute("SELECT id FROM files")
    cdn.file_index = set(file[0] for file in c.fetchall())

    c.execute("SELECT id FROM directories")
    cdn.dir_index = set(dir_[0] for dir_ in c.fetchall())

    c.execute("SELECT token FROM tokens")
    cdn.token_index = set(token[0] for token in c.fetchall())