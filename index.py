import psycopg

from constants.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, \
        DB_SCHEMA, XML_DIRECTORY
from create_schema import create_schema
from create_tables import create_tables
from recursion import recursion

with psycopg.connect(
            'dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}' \
            .format(dbname=DB_NAME, dbuser=DB_USER, dbpassword=DB_PASSWORD, dbhost=DB_HOST, dbport=DB_PORT)
        ) as conn:
    with conn.cursor() as cur:
        #create_schema(cur, conn, DB_SCHEMA)
        #create_tables(cur, conn, DB_SCHEMA)
        recursion(cur, conn, XML_DIRECTORY, DB_SCHEMA)
