import mysql.connector

def get_database_connection():
    # Replace the connection parameters with your actual database credentials
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="blogx"
    )
    return conn