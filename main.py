from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select

# from dto.post_dto import PostDto

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str

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

app = FastAPI()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()

@app.get('/')
def getHello():
    return 'Hello World'


@app.post('/posts', status_code=201)
def create_post(blog: Post, session: SessionDep):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@app.get('/posts')
def find_all(session: SessionDep):
    return session.exec(select(Post)).all()

@app.get('/posts/{id}')
def find_one_by_id(id: int, session: SessionDep):
    return session.get(Post, id)

@app.delete('/posts/{id}', status_code=204)
def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    session.delete(post)
    session.commit()
