from includes.connection import get_database_connection


def read_all_categories():
    conn = get_database_connection()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM categories")
    
    # Fetch all rows from the database and convert them to dictionaries with appropriate keys
    columns = [col[0] for col in mycursor.description]
    categories = [dict(zip(columns, row)) for row in mycursor.fetchall()]
    
    conn.close()
    return {"categories": categories}