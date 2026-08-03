from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select

from posts.dto.create_post_dto import CreatePostDto
from posts.dto.update_post_dto import UpdatePostDto
from posts.entities.post_entity import Post
from common.dto.pagination_dto import PaginationDto


sqlite_file_name = 'blogging_platform.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


class PostsService:

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def create_post(self, create_post_dto: CreatePostDto):
        post = Post(**create_post_dto.model_dump())
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def find_all_posts(self, pagination_dto: PaginationDto):
        pagination_dict = pagination_dto.model_dump()
        limit = pagination_dict['limit']
        page = pagination_dict['page'] - 1
        return self.session.exec(select(Post).offset(page * limit).limit(limit)).all()

    def find_one_post(self, id: int):
        post = self.session.get(Post, id)
        if not post:
            raise HTTPException(status_code=404, detail=f'The post with ID #{ id } not found')
        return post

    def update_post(self, id: int, update_post_dto: UpdatePostDto):
        post = self.find_one_post(id)
        post_data = update_post_dto.model_dump(exclude_none=True)
        post.sqlmodel_update(post_data)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete_post(self, id: int):
        post = self.find_one_post(id)
        
        self.session.delete(post)
        self.session.commit()