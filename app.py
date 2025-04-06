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

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

####  nakano add Start  ####
# .envファイルを読み込む
load_dotenv()

client = OpenAI()

###　●●●　Local用　　●●●
# 環境変数からAPIキーを取得

OpenAI.api_key = os.getenv("OPENAI_API_KEY")
kokudo_api_key = os.getenv("kokudo_API_KEY")
###　●●●　Host用　　●●●
# シークレットからAPIキーを取得
# OpenAI.api_key  = st.secrets["OPENAI_API_KEY"]

def send_request(query: str) -> dict:

    END_POINT: str = "https://www.mlit-data.jp/api/v1/"
    
    response: requests.models.Response = requests.post(
        END_POINT,
        headers={
            "Content-type": "application/json",
            "apikey": kokudo_api_key,
        },
        json={"query": query},
    )
    result: dict = json.loads(response.content)["data"]
    return result

query_ken_string = '''
    query {
        prefecture {
            code
            name
        }
    }
    '''

query_city_string = '''
    query{
        municipalities {
            code
            prefecture_code
            name
        }
    }
    '''
    
data: dict = send_request(query=query_ken_string)
df_ken: pd.DataFrame = pd.json_normalize(data["prefecture"])
df_ken['code_str'] = df_ken['code'].astype(str).str.zfill(2)
df_ken['codename'] = df_ken['code_str'].str.cat(df_ken['name'], sep=' ')

data: dict = send_request(query=query_city_string)
df_city: pd.DataFrame = pd.json_normalize(data["municipalities"])
df_merge= pd.merge(df_ken,df_city,left_on='code',right_on='prefecture_code')
area_data = df_merge.groupby("codename")["name_y"].apply(list).to_dict()

# データインポート
df = pd.read_csv("https://www.soumu.go.jp/main_content/000420038.csv", encoding="shift_jis")
df_dai = df[df['中分類コード']==0];
df_chu = df[(df['小分類コード']==0) & (df['中分類コード']!=0)];
df_chu['大分類コード'] =df_chu['大分類コード'].astype(str)
df_dai['大分類コード'] =df_dai['大分類コード'].astype(str)
df_dai['codename1']= df_dai['大分類コード'].str.cat(df_dai['項目名'],sep=' ');

df_gyou_join= pd.merge(df_chu,df_dai,on = '大分類コード')

# area_data = df_gyou_join.groupby("codename1")["項目名_y"].apply(list).to_dict()
industry_data = df_gyou_join.groupby("codename1")["項目名_x"].apply(list).to_dict()

# nakano add End

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

@app.post("/customers")
def create_customer(customer: Customer):
    print("nakano create_customer")
    values = customer.dict()
    
    # add nakano Start
    tmp_id = values.get("customer_id")
    if tmp_id == '':
        return None
        raise HTTPException(status_code=404, detail="Customer not create")
    # add nakano End
    
    tmp = crud.myinsert(mymodels_MySQL.Customers, values)
    result = crud.myselect(mymodels_MySQL.Customers, values.get("customer_id"))

    if not result:
        raise HTTPException(status_code=404, detail="Customer not create")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None
#    return None

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
