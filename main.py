from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# define a Pydantic model for the data to be inserted
client = MongoClient("mongodb://localhost:27017/")

# select the database and collection
db = client["mydatabase"]
questions = db["questions"]
items = db["items"]

class Item(BaseModel):
    name: str
    description: str

class Question(BaseModel):
    name: str
    question: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
app = FastAPI()

@app.get("/questions/")
async def get_question():
    result = questions.find({})
    res = []
    for i in result:
        i['id'] = str(i['_id'])
        del i['_id']
        res.append(i)
        
    json_able = jsonable_encoder({"result": res})
    return JSONResponse(content=json_able)


@app.post("/questions/")
async def create_question(question: Question):
    result = questions.insert_one(question.dict())
    
    return JSONResponse({
        'message':'question created successfully',
        'result': {
            'id': str(result.inserted_id)
        },
    }, 201)


@app.get("/")
async def root():
    return {'result': "ok"}