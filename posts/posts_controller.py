from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlmodel import create_engine, SQLModel, Session, select

from posts.entities.post_entity import Post
from posts.dto.create_post_dto import CreatePostDto
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

SessionDep = Annotated[Session, Depends(get_session)]


posts_controller = APIRouter()

@posts_controller.on_event('startup')
def on_startup():
    create_db_and_tables()


@posts_controller.post('/posts', status_code=201, response_model=Post)
def create_post(create_post_dto: CreatePostDto, session: SessionDep):
    post = Post(**create_post_dto.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@posts_controller.get('/posts')
def find_all(session: SessionDep, pagination_dto: Annotated[PaginationDto, Query()]):
    pagination_dict = pagination_dto.model_dump()
    limit = pagination_dict['limit']
    page = pagination_dict['page'] - 1
    return session.exec(select(Post).offset(page * limit).limit(limit)).all()

@posts_controller.get('/posts/{id}')
def find_one_by_id(id: int, session: SessionDep):
    return session.get(Post, id)

@posts_controller.delete('/posts/{id}', status_code=204)
def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    session.delete(post)
    session.commit()
