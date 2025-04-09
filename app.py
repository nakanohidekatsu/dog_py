from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import pandas as pd
import json
from graphene import ObjectType, String, Int, List, Schema, Mutation, Field
import os
from db_control import crud, mymodels_MySQL
from db_control.create_tables_MySQL import init_db
from dotenv import load_dotenv

"""
# # アプリケーション初期化時にテーブルを作成
init_db()

"""

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.get("/profile")
def read_dog_profile(dog_id: str = Query(...)):
    result = crud.dogselect(mymodels_MySQL.profile, dog_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dog_profile not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.get("/recommend_misic")
def read_recommend_misic(dog_id: str = Query(...)):
    result = crud.historyselect(mymodels_MySQL.history_tbl, dog_id)
    if not result:
        raise HTTPException(status_code=404, detail="history_tbl not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.get("/get_misic")
def read_music_tbl(souund_id: str = Query(...)):
    result = crud.soundselect(mymodels_MySQL.music_tbl, souund_id)
    if not result:
        raise HTTPException(status_code=404, detail="souund_id not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

