from psycopg import cursor, connection

def create_schema(cur: cursor, conn: connection, name: str) -> None:
    """Создает в БД новую схему (если схемы с таким именем ещё нет)

    :param cur: _description_
    :type cur: cursor
    :param conn: _description_
    :type conn: connection
    :param name: _description_
    :type name: str
    """
    cur.execute("CREATE SCHEMA IF NOT EXISTS {schema} AUTHORIZATION kotelevsky;GRANT ALL ON SCHEMA {schema} TO cadaster;GRANT ALL ON SCHEMA {schema} TO kotelevsky;" \
        .format(schema=name))
    print('--- Создана схема {schema} ---'.format(schema=name))

    conn.commit()