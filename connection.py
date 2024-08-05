import psycopg

def connectToDB(dbhost, dbport, dbuser, dbpassword, dbname):
    try:
        connection = psycopg.connect(
            'dbname={dbname} user={dbuser} password={dbpassword} host={dbhost} port={dbport}' \
            .format(dbname=dbname, dbuser=dbuser, dbpassword=dbpassword, dbhost=dbhost, dbport=dbport)
        )
        print('--- Соединение с БД установлено ---')
    except psycopg.Error as e:
        print(e)
    cursor = connection.cursor()

    connection.commit()
    return connection, cursor