from includes.connection import get_database_connection
from model.Post import Post

def read_all():
    conn = get_database_connection()
    
    post_model = Post(conn)
    posts = post_model.read()
    
    conn.close()
    return {"posts": posts}


def read_one(post_id: int):
    conn = get_database_connection()
    # mycursor = conn.cursor()
    # mycursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    
    # columns = [col[0] for col in mycursor.description]
    # post = mycursor.fetchone()
    
    post_model = Post(conn)
    post = post_model.read_single(post_id)
    
    conn.close()

    if not post:
        # raise HTTPException(status_code=404, error="Post not found")
        # Return the status code and details in the response dictionary
        return {"status_code": 404, "error": "Post not found"}
    
    return post


def add_post(post_data):
    conn = get_database_connection()
    mycursor = conn.cursor()
    
    # Execute the query to insert a new post into the database
    query = "INSERT INTO posts (title, body, author, category_id) VALUES (%s, %s, %s, %s)"
    values = (post_data.title, post_data.body, post_data.author, post_data.category_id)
    mycursor.execute(query, values)
    conn.commit()

    # Get the ID of the newly inserted post
    post_id = mycursor.lastrowid

    conn.close()

    # Return the created post data including the new ID
    return {**post_data.dict(), "id": post_id}


def edit_post(post_id, updated_post_data):
    conn = get_database_connection()
    mycursor = conn.cursor()
    
    # Check if the post exists before updating
    mycursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    existing_post = mycursor.fetchone()
    if not existing_post:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Update the post with the new data
    update_query = "UPDATE posts SET title = %s, body = %s, author = %s, category_id = %s WHERE id = %s"
    update_values = (
        updated_post_data.get("title"),
        updated_post_data.get("body"),
        updated_post_data.get("author"),
        updated_post_data.get("category_id"),
        post_id
    )
    mycursor.execute(update_query, update_values)
    conn.commit()
    
    conn.close()

    return {"message": "Post updated successfully"}


def delete_post(post_id: int):
    conn = get_database_connection()
    mycursor = conn.cursor()
    
    # Check if the post exists before deleting
    mycursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    existing_post = mycursor.fetchone()
    if not existing_post:
        conn.close()
        # raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post not found"}
    
    # Delete the post with the given ID
    mycursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    
    conn.commit()
    
    conn.close()

    return {"message": "Post deleted successfully"}