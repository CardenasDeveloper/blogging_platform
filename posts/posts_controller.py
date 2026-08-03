from typing import Annotated
from fastapi import APIRouter, Depends, Query

from posts.entities.post_entity import Post
from posts.dto.create_post_dto import CreatePostDto
from posts.posts_service import PostsService, create_db_and_tables
from common.dto.pagination_dto import PaginationDto


posts_controller = APIRouter()

@posts_controller.on_event('startup')
def on_startup():
    create_db_and_tables()


@posts_controller.post('/posts', status_code=201, response_model=Post)
def create_post(create_post_dto: CreatePostDto, postsService: Annotated[PostsService, Depends(PostsService)]):
    return postsService.create_post(create_post_dto)

@posts_controller.get('/posts', response_model=list[Post])
def find_all(pagination_dto: Annotated[PaginationDto, Query()], postsService: Annotated[PostsService, Depends(PostsService)]):
    return postsService.find_all_posts(pagination_dto)

@posts_controller.get('/posts/{id}', response_model=Post)
def find_one_post(id: int, postsService: Annotated[PostsService, Depends(PostsService)]):
    return postsService.find_one_post(id)

@posts_controller.delete('/posts/{id}', status_code=204)
def delete_post(id: int, postsService: Annotated[PostsService, Depends(PostsService)]):
    return delete_post(id)
    
