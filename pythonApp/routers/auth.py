from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from models import Users

router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    password: str
    role: str


@router.post("/auth")
async def create_user(createUserRequest: CreateUserRequest):
    createUserModel = Users(
        # não posso fazer igual fiz em todos porque aqui eu possuo o password, no models, eu tenho o hashed_password
        ## o que ta na esquerda vem do models, o que ta na direita vem da classe q acabei de criar. 
        ## Cuidado porque o nome deve ser igual
        ## tanto para o que vem de models como o q vem da classe
        email=createUserRequest.email,
        userName=createUserRequest.username,
        firstName=createUserRequest.firstName,
        lastName=createUserRequest.lastName,
        role=createUserRequest.role,
        hashedPassword=createUserRequest.password,
        isActive=True
    )
    return createUserModel
