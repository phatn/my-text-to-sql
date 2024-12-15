from db_connection import get_connection


def get_schema():
    connection = get_connection()

    # Establish connection to MySQL
    schema = ""
    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Query to get all table names from the database
    cursor.execute("SHOW TABLES")

    # Fetch all tables
    tables = cursor.fetchall()

    # Iterate over all tables
    for i in range(0, len(tables)):
        table_name = tables[i][0]
        # print(f"Table: {table_name}")
        schema += f'CREATE TABLE {table_name}('
        # Query to get columns and their data types for the current table
        cursor.execute(f"DESCRIBE {table_name}")

        # Fetch all columns and data types
        columns = cursor.fetchall()
        for j in range(0, len(columns)):
            name = columns[j][0]
            data_type = columns[j][1]
            schema += f"{name} {data_type}"
            if j == len(columns) - 1 and i == len(tables) - 1:
                schema += ")"
            elif j == len(columns) - 1:
                schema += "); "
            else:
                schema += ", "
    cursor.close()
    connection.close()
    return schema


def execute_query(query):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    connection.close()
    return columns, [dict(zip(columns, row)) for row in rows]


def validate_sql(sql_query):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"EXPLAIN {sql_query}")
        cursor.fetchall()
        return True, ""
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        connection.close()


def login(email, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = f"SELECT fullname FROM users WHERE email = '{email}' AND password = '{password}'"
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    if row is None:
        return False, []
    return True, row
