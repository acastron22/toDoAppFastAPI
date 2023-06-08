from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import ToDos
from database import SessionLocal



router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# aqui está sendo criado o request do post. O que o post precisa ter para aceitar(os nomes devem
# ser os mesmos que as colunas das tabelas)
class todoRequest(BaseModel):

    # o field cria request, no caso estou dizendo q o comprimento mínimo é de 3 caracteres
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    # o validador diz q tem q ser maior que 0 e menor que 6
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(ToDos).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

# criando o post request


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: todoRequest):
    todo_model = ToDos(**todo_request.dict())
    db.add(todo_model)
    db.commit()

# Agora q eu tenho o método post, preciso de um método de delete


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      todo_request: todoRequest,
                      todo_id: int = Path(gt=0)):
    # verifico se o id que passo é igual ao id existente na tabela
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# Última etapa do CRUD agora é criar um DELETE
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()

    db.commit()

# Com isso, todas as etapas do CRUD estão finalizadas
