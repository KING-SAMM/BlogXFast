# Refactored - MVC pattern
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from model.schema import PostCreate  # Import the PostCreate model

from api.post import read_all, read_one, add_post, edit_post, delete_post
from api.category import read_all_categories

app = FastAPI()

# Set up CORS middleware to allow requests from http://127.0.0.1:5503
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5503", "http://127.0.0.1:8002"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Specify allowed HTTP methods
    allow_headers=["X-Requested-With", "Content-Type", "Authorization"], # Specify allowed headers
)

# Routes
@app.get("/")
def root():
    conn = get_database_connection()
    mycursor = conn.cursor()
    mycursor.execute("SHOW DATABASES")
    databases = [x[0] for x in mycursor]
    conn.close()
    return {"databases": databases}

@app.get("/categories")
def get_categories():
    return read_all_categories()

@app.get("/posts")
def get_posts():
    return read_all()


@app.get("/posts/{post_id}")
def get_single_post(post_id: int):
    return read_one(post_id)


@app.post("/posts", response_model=PostCreate)
def create_post(post_data: PostCreate):
    return add_post(post_data)


@app.put("/posts/{post_id}")
def update_post(post_id: int, updated_post_data: dict):
    return edit_post(post_id, updated_post_data)


@app.delete("/posts/{post_id}")
def delete_single_post(post_id: int):
    return delete_post(post_id)


