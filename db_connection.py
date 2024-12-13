from mysql.connector import pooling
from mysql.connector import errors
import time

import mysql.connector

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,  # Adjust as needed
    pool_reset_session=True,
    **{
        "host": "127.0.0.1",
        "port": "3306",
        "user": "root",
        "password": "p@ssword",
        "database": "retailers"
    }
)


def get_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="p@ssword",
        database="retailers"
    )
    return connection
