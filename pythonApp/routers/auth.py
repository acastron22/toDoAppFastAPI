from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# pacote usado para usar o hashpasswords
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '302c43590b5cebc3125b2e771b66d8d8e5089eb8ff7a8791513e6019a1122608'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2Bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str

    # devemos ter um db dependency, igual ao todos, para poder armazenar as informações de usuário na tabela


class Token(BaseModel):
    accessToken: str
    tokenType: str


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
    return user


def createAccessToken(username: str, userId: int, expiresDelta: timedelta):
    encode = {'sub': username, 'id': userId}
    expires = datetime.utcnow() + expiresDelta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def getCurrentUser(token: Annotated[str, Depends(oauth2Bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        userId: int = payload.get('id')
        if username is None or userId is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': userId}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token)
async def loginForAccessToken(formData: Annotated[OAuth2PasswordRequestForm, Depends()],
                              db: db_dependency):
    user = authenticateUser(formData.username, formData.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = createAccessToken(user.userName, user.id, timedelta(minutes=20))

    return {'accessToken': token, 'tokenType': 'bearer'}
