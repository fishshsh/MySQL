import mysql.connector
import queries

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'store'
}

def create_connection(host, user, password, database=None):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host, user=user, password=password
        )
    except mysql.connector.Error:
        print('<-> Failed trying to CONNECT to the server!')
    else:
        print('<+> Connection was successfully established!')

    if connection and database:
        cursor = connection.cursor()

        try:
            cursor.execute(
                'CREATE DATABASE IF NOT EXISTS {};'.format(database)
            )
        except mysql.connector.Error:
            print('<-> Failed trying to CREATE the database!')
        else:
            print('<+> The database was successfully created!')
            cursor.execute('USE {};'.format(database))

        cursor.close()

    return connection

def execute_create_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except mysql.connector.Error:
        print('<-> Failed trying to CREATE the table!')
    else:
        print('<+> The table was successfully created!')

    cursor.close()
    return None

def execute_insert_query(connection, query, rows):
    cursor = connection.cursor()

    try:
        cursor.executemany(query, rows)
    except mysql.connector.Error as error:
        print('<-> Failed trying to INSERT rows INTO the table!')
    else:
        print('<+> Rows was successfully inserted!')

    cursor.close()
    return None

def execute_select_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except mysql.connector.Error:
        print('<-> Failed trying to SELECT rows FROM the table!')
    else:
        print('<+> Rows was successfully selected!')

    selected = cursor.fetchall()

    cursor.close()
    return selected

def execute_update_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except mysql.connector.Error:
        print('<-> Failed trying to UPDATE rows in the table!')
    else:
        print('<+> Rows was successfully updated!')

    cursor.close()
    return None

def execute_drop_query(connection, query):
    cursor = connection.cursor()

    try:
        cursor.execute(query)
    except mysql.connector.Error:
        print('<-> Failed trying to DROP the table!')
    else:
        print('<+> The table was successfully dropped!')

    cursor.close()
    return None

def execute_main_script(config):
    print('Connecting to the server...')
    connection = create_connection(*config.values())
    if not connection:
        return None

    connection.autocommit = True

    print('\nExecuting CREATE queries...')
    for query in queries.queries['CREATE']:
        execute_create_query(connection, query)
    
    print('\nExecuting INSERT queries...')
    for query, rows in queries.queries['INSERT']:
        execute_insert_query(connection, query, rows)

    print('\nExecuting SELECT queries...')
    for query in queries.queries['SELECT']:
        selected = execute_select_query(connection, query)
        print('\nSelected rows:', *selected, sep='\n')

    print('\nExecuting UPDATE queries...')
    for query in queries.queries['UPDATE']:
        execute_update_query(connection, query)

    print('\nExecuting DROP queries...')
    for query in queries.queries['DROP']:
        execute_drop_query(connection, query)

    connection.close()
    return None

if __name__ == '__main__':
    execute_main_script(config)
