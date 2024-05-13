from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse

import requests

app = FastAPI()

# Define data model
class Post(BaseModel):
    title: str
    content: str
    author: str
    created_at: datetime = datetime.now()

# Mock data
posts = []

# CRUD operations
@app.post("/posts/")
def create_post(post: Post):
    posts.append(post)
    return post

@app.get("/posts/", response_model=List[Post])
def get_posts():
    return posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if post_id < len(posts):
        return posts[post_id]
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    if post_id < len(posts):
        posts[post_id] = post
        return {"message": "Post updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    if post_id < len(posts):
        deleted_post = posts.pop(post_id)
        return {"message": "Post deleted successfully", "deleted_post": deleted_post}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Handler for root path
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Welcome to the FastAPI blog!</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI blog!</h1>
            <p>This is a simple blog created using FastAPI.</p>
        </body>
    </html>
    """

# Handler for fetching external content
@app.get("/external-content")
def get_external_content():
    url = "https://www.python.org"  # Python's official website

    html_content = fetch_webpage(url)
    parsed_content = parse_webpage(html_content)
    return parsed_content

# Functions for fetching and parsing webpage content
def fetch_webpage(url):
    response = requests.get(url)
    return response.text

def parse_webpage(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup.find_all('p')
