from fastapi import FastAPI

from posts.posts_controller import posts_controller

app = FastAPI()

app.include_router(posts_controller)