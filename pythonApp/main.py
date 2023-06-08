from fastapi import FastAPI  
import models
from database import engine
from routers import auth, todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

##Preciso indicar a importação do router para incluir na minha API o auth.py
app.include_router(auth.router)
app.include_router(todos.router)
