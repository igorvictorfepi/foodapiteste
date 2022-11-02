from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
 
DATABASE_URL = "postgresql://jvqdzdgtbewwtv:274563f8fc0024dae7fc84b27c00cc7a593f9506775a146f2b1934bd1d5108d7@ec2-54-163-34-107.compute-1.amazonaws.com:5432/d4eq052nm6qqfd"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

app = FastAPI()

menu = sqlalchemy.Table(
    "menu",
    metadata,
    sqlalchemy.Column("nome", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("img", sqlalchemy.String),
)

class Menu(BaseModel):
    nome: str
    img: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
  
@app.get("/menu/", response_model=List[Menu])   
async def read_restaurantes():
    query = menu.select()
    return await database.fetch_all(query) 
    