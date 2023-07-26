# import sqlite3
from includes.connection import get_database_connection

class Post:
    def __init__(self, db_path):
        # DB stuff
        # self.conn = sqlite3.connect(db_path)
        self.conn = db_path
        self.table = 'posts'


    # Get Posts
    def read(self):
        query = f"""
            SELECT 
                c.name as category_name, 
                p.id, 
                p.category_id, 
                p.title, 
                p.body, 
                p.author, 
                p.created_at 
            FROM 
                {self.table} p 
            LEFT JOIN 
                categories c 
            ON 
                p.category_id = c.id 
            ORDER BY 
                p.created_at DESC
        """
        
        mycursor = self.conn.cursor()
        mycursor.execute(query)
        columns = [col[0] for col in mycursor.description]
        posts = [dict(zip(columns, row)) for row in mycursor.fetchall()]
        return posts
    
    
    # Read Single Post
    def read_single(self, post_id):
        query = f"""
            SELECT 
                c.name as category_name, 
                p.id, 
                p.category_id, 
                p.title, 
                p.body, 
                p.author, 
                p.created_at 
            FROM 
                {self.table} p 
            LEFT JOIN 
                categories c 
            ON 
                p.category_id = c.id 
            WHERE
                p.id = %s
            LIMIT
                1
        """
        
        mycursor = self.conn.cursor()
        mycursor.execute(query, (post_id,))
        
        columns = [col[0] for col in mycursor.description]
        row = mycursor.fetchone()    
        
        if row is None:
            # Return an error message indicating that the post with the specified ID does not exist
            return {"error": "The resource does not exist."}
        
        return dict(zip(columns, row))
        

