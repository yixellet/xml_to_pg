from psycopg import cursor, connection
import re

from constants.fields import FIELDS

def insert_into_table(cur: cursor, conn: connection, 
                      object: dict, schema: str) -> None:
    #print(object)
    table_name = object['content'] + '__' + object['crs']
    object_desc = FIELDS[object['content']]

    fields_ = []
    set_fields_ = []
    values_ = []

    if object['crs'] != 'no_geometry':
        fields_.append("geom")
        set_fields_.append("geom = EXCLUDED.geom")
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
    """if object['cad_number'] == '30:08:110107:104':
        print(object)
        
        print(
            f""
            INSERT INTO {schema}."{table_name}" as x ({','.join(fields_)}) 
            VALUES ({','.join(values_)}) 
            ON CONFLICT ("{object_desc['unique']}") DO UPDATE
            SET {','.join(set_fields_)}
            WHERE x."date_formation" < EXCLUDED."date_formation";
            ""
        )"""
    cur.execute(
        f"""
        INSERT INTO {schema}."{table_name}" as x ({','.join(fields_)}) 
        VALUES ({','.join(values_)}) 
        ON CONFLICT ("{object_desc['unique']}") DO UPDATE
        SET {','.join(set_fields_)}
        WHERE x."date_formation" < EXCLUDED."date_formation";
        """
    )
    conn.commit()
    #print('--- Таблицы заполнены ---')