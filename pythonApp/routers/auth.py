from typing import Annotated
from fastapi import Depends, APIRouter
from starlette import status
from pydantic import BaseModel
from models import Users
from sqlalchemy.orm import Session
# pacote usado para usar o hashpasswords
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str

    # devemos ter um db dependency, igual ao todos, para poder armazenar as informações de usuário na tabela


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticateUser(username: str, password: str, db):
    user = db.query(Users).filter(Users.userName == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashedPassword):
        return False
    return True


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      createUserRequest: CreateUserRequest):
    createUserModel = Users(
        # não posso fazer igual fiz em todos porque aqui eu possuo o password, no models, eu tenho o hashed_password
        # o que ta na esquerda vem do models, o que ta na direita vem da classe q acabei de criar.
        # Cuidado porque o nome deve ser igual
        # tanto para o que vem de models como o q vem da classe
        email=createUserRequest.email,
        userName=createUserRequest.username,
        firstName=createUserRequest.firstName,
        lastName=createUserRequest.lastName,
        role=createUserRequest.role,
        hashedPassword=bcrypt_context.hash(createUserRequest.password),
        isActive=True
    )
    db.add(createUserModel)
    db.commit()


@router.post("/token")
async def loginForAcessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()],
                             db: db_dependency):
    user = authenticateUser(formData.username, formData.password, db)
    if not user:
        return 'Failed authentication'
    return 'Successful authentication'
    return formData.username
