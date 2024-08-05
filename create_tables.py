from psycopg import cursor, connection

from constants.msk_zones import MSK_ZONES
from constants.fields import FIELDS

def create_tables(cur: cursor, conn: connection, schema: str) -> None:
    for zone in MSK_ZONES['30'].keys():
        for object in FIELDS.values():
            for geom_type in object['geom_types']:
                fields = []
                comments = []
                for field in object['fields']:
                    field_str = f""""{field['name']}" {field['type']}{' COLLATE pg_catalog."default"' if field['type'] == 'text' else ''}"""
                    fields.append(field_str)
                    comment = f"""COMMENT ON COLUMN {schema}."{object['name']}__30.{zone}"."{field['name']}" IS '{field['desc']}';"""
                    comments.append(comment)
                #print(comments)
                
                cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS {schema}."{object['name']}__30.{zone}"
                    (
                        geom geometry({geom_type}),
                        {','.join(fields)},
                        uid uuid NOT NULL DEFAULT gen_random_uuid(),
                        CONSTRAINT "{object['name']}__30.{zone}_pkey" PRIMARY KEY (uid),
                        CONSTRAINT "{object['name']}__30.{zone}_{object['unique']}_key" UNIQUE ({object['unique']})
                    )

                    TABLESPACE pg_default;

                    ALTER TABLE IF EXISTS {schema}."{object['name']}__30.{zone}"
                        OWNER to postgres;

                    COMMENT ON TABLE {schema}."{object['name']}__30.{zone}"
                        IS '{object['desc']} МСК-30 зона {zone}';
                    
                    {' '.join(comments)}

                    CREATE INDEX IF NOT EXISTS "sidx_{object['name']}__30.{zone}_geom"
                        ON {schema}."{object['name']}__30.{zone}" USING gist
                        (geom)
                        TABLESPACE pg_default;""")
                conn.commit()
                
    
    print('--- Созданы таблицы в БД ---')
