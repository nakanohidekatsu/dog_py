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
from openai import OpenAI

"""
# # アプリケーション初期化時にテーブルを作成
init_db()

class Customer(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str

class Sales(BaseModel):
    customer_name: str
    customer_id: str
    ken: str
    city: str
    sicName: str
    simcName: str
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

"""
@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None


@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels_MySQL.Customers)
    # 結果がNoneの場合は空配列を返す
    if not result:
        return []
#        return ([])
    # JSON文字列をPythonオブジェクトに変換
    return json.loads(result)


@app.put("/customers")
def update_customer(customer: Customer):
    values = customer.dict()
    values_original = values.copy()
    tmp = crud.myupdate(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values_original.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

# add nakano Start
@app.get("/sales")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.mysalesselect(mymodels_MySQL.Sales, customer_id)
    if not result:
        result_obj =[{
            "customer_id": customer_id,
            "customer_name": "",
            "ken": "",
            "city": "",
            "sicName": "",
            "simcName": "",
        }]
    else:
        try:
            result_obj = json.loads(result)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format from database"}
    return result_obj[0] if result_obj else None

@app.put("/sales_update")
def update_sales(sales: Sales):
    values = sales.dict()
    values_original = values.copy()
    
    print("nakano salesinsert sales_update values_original",values_original)
    
    tmp = crud.mydelete(mymodels_MySQL.Sales, values_original.get("customer_id"))
    tmp = crud.mysalesinsert(mymodels_MySQL.Sales, values_original)
    result = crud.mysalesselect(mymodels_MySQL.Sales, values_original.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.get("/industries")
def get_industries():
    return {"categories": list(industry_data.keys())}

@app.get("/sub-industries/{category}")
def get_sub_industries(category: str):
    sub_categories = industry_data.get(category, [])
    return {"sub_categories": sub_categories}

@app.get("/ken")
def get_ken():
    return {"kens": list(area_data.keys())}

@app.get("/cities/{ken}")
def get_sub_industries(ken: str):
    cities = area_data.get(ken, [])
    return {"cities": cities}

#app.delete("/sales_delete")
#def delete_sales(customer_id: str = Query(...)):
#    result = crud.mysalesdelete(mymodels_MySQL.Sales, customer_id)
#    if not result:
#        raise HTTPException(status_code=404, detail="Customer not found")
#    return {"customer_id": customer_id, "status": "deleted"}

# add nakano End

@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()

"""