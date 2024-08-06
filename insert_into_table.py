from psycopg import cursor, connection

from constants.fields import FIELDS

def insert_into_table(cur: cursor, conn: connection, 
                      object: dict, schema: str) -> None:
    table_name = object['content'] + '__' + object['crs']
    object_desc = FIELDS[object['content']]
    fields = []
    set_fields = []
    for field in object_desc['fields']:
        fields.append(f"""\"{field['name']}\"""")
        set_fields.append(f"""\"{field['name']}\" = EXCLUDED.\"{field['name']}\"""")
    values = []
    for key, value in object.items():
        if key in object_desc['fields']:
            values.append(value)
    
    print(object['geom'])
    """
    cur.execute(
        f""
        INSERT INTO {schema}.{table_name} ({','.join(fields)}) 
        VALUES ({','.join(values)}) 
        ON CONFLICT ("{object_desc['unique']}") DO UPDATE 
        SET {','.join(set_fields)}
        WHERE date_formation < EXCLUDED.date_formation;
        ""
    )
    conn.commit()"""
    print('--- Таблицы заполнены ---')