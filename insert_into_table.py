from psycopg import cursor, connection
import re

from constants.fields import FIELDS

def insert_into_table(cur: cursor, conn: connection, 
                      object: dict, schema: str) -> None:
    table_name = object['content'] + '__' + object['crs']
    object_desc = FIELDS[object['content']]

    fields_ = []
    set_fields_ = []
    values_ = []

    if object['crs'] != 'no_geometry':
        fields_.append("geom")
        set_fields_.append("geom = ST_GeomFromText(EXCLUDED.geom)")
        values_.append(f"""ST_GeomFromText(\'{object['geom']}\')""")

    for key, value in object.items():
        if key in object_desc['fields']:
            fields_.append(f"""\"{key}\"""")
            set_fields_.append(f"""\"{key}\" = EXCLUDED.\"{key}\"""")
            if type(value) is int or type(value) is float or value == None:
                values_.append(str(value))
            else:
                string = re.sub(r'[\'\"]', ' ', str(value))
                values_.append(f"""\'{string}\'""")
    """
    print(
        f""
        INSERT INTO {schema}."{table_name}" as x ({','.join(fields_)}) 
        VALUES ({','.join(values_)}) 
        ON CONFLICT ("{object_desc['unique']}") DO NOTHING;
        ""
    )"""
    cur.execute(
        f"""
        INSERT INTO {schema}."{table_name}" as x ({','.join(fields_)}) 
        VALUES ({','.join(values_)}) 
        ON CONFLICT ("{object_desc['unique']}") DO NOTHING;
        """
    )
    conn.commit()
    #print('--- Таблицы заполнены ---')