from psycopg import cursor, connection

from constants.msk_zones import MSK_ZONES

def create_tables(cur: cursor, conn: connection, schema: str) -> None:
    for zone in MSK_ZONES['30'].keys():
        # -- Зоны и территории --
        cur.execute(
            """CREATE TABLE IF NOT EXISTS {s}."zones__30.{z}"
            (
                geom geometry(MultiPolygon),
                registration_number text COLLATE pg_catalog."default",
                registration_date timestamp without time zone,
                name_by_doc text COLLATE pg_catalog."default",
                type_boundary text COLLATE pg_catalog."default",
                type_zone text COLLATE pg_catalog."default",
                reg_numb_border text COLLATE pg_catalog."default",
                "number" text COLLATE pg_catalog."default",
                uid uuid NOT NULL DEFAULT gen_random_uuid(),
                CONSTRAINT "zones__30.{z}_pkey" PRIMARY KEY (uid),
                CONSTRAINT "zones__30.{z}_reg_numb_border_key" UNIQUE (reg_numb_border)
            )

            TABLESPACE pg_default;

            ALTER TABLE IF EXISTS {s}."zones__30.{z}"
                OWNER to postgres;

            COMMENT ON TABLE {s}."zones__30.{z}"
                IS 'Зоны и территории МСК-30 зона {z}';

            CREATE INDEX IF NOT EXISTS "sidx_zones__30.{z}_geom"
                ON {s}."zones__30.{z}" USING gist
                (geom)
                TABLESPACE pg_default;""".format(z=zone, s=schema))
        conn.commit()

        # -- Земельные участки --
        cur.execute(
            """CREATE TABLE IF NOT EXISTS {s}."lands__30.{z}"
            (
                geom geometry(MultiPolygon),
                registration_number text COLLATE pg_catalog."default",
                date_formation date,
                address text COLLATE pg_catalog."default",
                subtype text COLLATE pg_catalog."default",
                common_land_cad_number text COLLATE pg_catalog."default",
                cad_number text COLLATE pg_catalog."default",
                type text COLLATE pg_catalog."default",
                area_inaccuracy real,
                area real,
                area_type text COLLATE pg_catalog."default",
                land_use_by_document text COLLATE pg_catalog."default",
                land_use text COLLATE pg_catalog."default",
                land_use_mer text COLLATE pg_catalog."default",
                uid uuid NOT NULL DEFAULT gen_random_uuid(),
                CONSTRAINT "lands__30.{z}_pkey" PRIMARY KEY (uid),
                CONSTRAINT "lands__30.{z}_cad_number_key" UNIQUE (cad_number)
            )

            TABLESPACE pg_default;

            ALTER TABLE IF EXISTS {s}."lands__30.{z}"
                OWNER to postgres;

            COMMENT ON TABLE {s}."lands__30.{z}"
                IS 'Земельные участки МСК-30 зона {z}';

            CREATE INDEX IF NOT EXISTS "sidx_lands__30.{z}_geom"
                ON {s}."lands__30.{z}" USING gist
                (geom)
                TABLESPACE pg_default;""".format(z=zone, s=schema))
        conn.commit()

        # -- Кадастровые кварталы --
        cur.execute(
            """CREATE TABLE IF NOT EXISTS {s}."quarters__30.{z}"
            (
                geom geometry(MultiPolygon),
                cad_number text COLLATE pg_catalog."default",
                date_formation date,
                area real,
                uid uuid NOT NULL DEFAULT gen_random_uuid(),
                CONSTRAINT "quarters__30.{z}_pkey" PRIMARY KEY (uid),
                CONSTRAINT "quarters__30.{z}_cad_number_key" UNIQUE (cad_number)
            )

            TABLESPACE pg_default;

            ALTER TABLE IF EXISTS {s}."quarters__30.{z}"
                OWNER to postgres;

            COMMENT ON TABLE {s}."quarters__30.{z}"
                IS 'Кадастровые кварталы МСК-30 зона {z}';

            CREATE INDEX IF NOT EXISTS "quarters__30.{z}_geom"
                ON {s}."quarters__30.{z}" USING gist
                (geom)
                TABLESPACE pg_default;""".format(z=zone, s=schema))
        conn.commit()

        # -- Границы муниципальные --
        cur.execute(
            """CREATE TABLE IF NOT EXISTS {s}."boundaries__30.{z}"
            (
                geom geometry(MultiPolygon),
                registration_number text COLLATE pg_catalog."default",
                date_formation date,
                registration_date timestamp without time zone,
                reg_numb_border text COLLATE pg_catalog."default",
                type_boundary text COLLATE pg_catalog."default",
                uid uuid NOT NULL DEFAULT gen_random_uuid(),
                CONSTRAINT "boundaries__30.{z}_pkey" PRIMARY KEY (uid),
                CONSTRAINT "boundaries__30.{z}_reg_numb_border_key" UNIQUE (reg_numb_border)
            )

            TABLESPACE pg_default;

            ALTER TABLE IF EXISTS {s}."boundaries__30.{z}"
                OWNER to postgres;

            COMMENT ON TABLE {s}."boundaries__30.{z}"
                IS 'Границы муниципальные МСК-30 зона {z}';

            CREATE INDEX IF NOT EXISTS "boundaries__30.{z}_geom"
                ON {s}."boundaries__30.{z}" USING gist
                (geom)
                TABLESPACE pg_default;""".format(z=zone, s=schema))
        conn.commit()

        # -- Береговые линии --
        cur.execute(
            """CREATE TABLE IF NOT EXISTS {s}."coastlines__30.{z}"
            (
                geom geometry(MultiPolygon),
                registration_number text COLLATE pg_catalog."default",
                date_formation date,
                registration_date timestamp without time zone,
                reg_numb_border text COLLATE pg_catalog."default",
                water text COLLATE pg_catalog."default",
                uid uuid NOT NULL DEFAULT gen_random_uuid(),
                CONSTRAINT "coastlines__30.{z}_pkey" PRIMARY KEY (uid),
                CONSTRAINT "coastlines__30.{z}_reg_numb_border_key" UNIQUE (reg_numb_border)
            )

            TABLESPACE pg_default;

            ALTER TABLE IF EXISTS {s}."coastlines__30.{z}"
                OWNER to postgres;

            COMMENT ON TABLE {s}."coastlines__30.{z}"
                IS 'Береговые линии МСК-30 зона {z}';

            CREATE INDEX IF NOT EXISTS "coastlines__30.{z}_geom"
                ON {s}."coastlines__30.{z}" USING gist
                (geom)
                TABLESPACE pg_default;""".format(z=zone, s=schema))
        conn.commit()
    
    print('--- Созданы таблицы в БД ---')
