from psycopg import cursor, connection

from constants.msk_zones import MSK_ZONES
from constants.fields import FIELDS

def create_tables(cur: cursor, conn: connection, schema: str) -> None:
    for zone in MSK_ZONES['30'].keys():
        zone_ = zone if zone == 'no_geometry' else f'30.{zone}'
        #print(zone_)
        for object in FIELDS.values():
            for geom_type in object['geom_types']:
                fields = []
                comments = []
                for field in object['fields'].values():
                    field_str = f""""{field['name']}" {field['type']}{' COLLATE pg_catalog."default"' if field['type'] == 'text' else ''}"""
                    fields.append(field_str)
                    comment = f"""COMMENT ON COLUMN {schema}."{object['name']}__{zone_}"."{field['name']}" IS '{field['desc']}';"""
                    comments.append(comment)
                #print(comments)

                index_string = f"""CREATE INDEX IF NOT EXISTS "sidx_{object['name']}__{zone_}_geom"
                        ON {schema}."{object['name']}__{zone_}" USING gist
                        (geom)
                        TABLESPACE pg_default""" if zone != 'no_geometry' else ''
                
                cur.execute(
                    f"""CREATE TABLE IF NOT EXISTS {schema}."{object['name']}__{zone_}"
                    (
                        {f'geom geometry({geom_type}),' if zone != 'no_geometry' else ''}
                        {','.join(fields)},
                        uid uuid NOT NULL DEFAULT uuid_generate_v4(),
                        CONSTRAINT "{object['name']}__{zone_}_pkey" PRIMARY KEY (uid),
                        CONSTRAINT "{object['name']}__{zone_}_{object['unique']}_key" UNIQUE ({object['unique']})
                    )

                    TABLESPACE pg_default;

                    ALTER TABLE IF EXISTS {schema}."{object['name']}__{zone_}"
                        OWNER to kotelevsky;

                    GRANT ALL ON TABLE {schema}."{object['name']}__{zone_}" TO cadaster;

                    GRANT ALL ON TABLE {schema}."{object['name']}__{zone_}" TO kotelevsky;

                    COMMENT ON TABLE {schema}."{object['name']}__{zone_}"
                        IS '{object['desc']} МСК-30 зона {zone_}';
                    
                    {' '.join(comments)}

                    {index_string};""")
                conn.commit()
                
    
    print('--- Созданы таблицы в БД ---')
