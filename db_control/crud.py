# uname() error回避
import platform
print("platform", platform.uname())

from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from db_control.connect_MySQL import engine
from db_control.mymodels_MySQL import Customers

def myinsert(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    
    query = insert(mymodel).values(values)
    print("nakano myinsert query")

    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return "inserted"

def dogselect(mymodel, dog_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.dog_id == dog_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for profile in result:
            result_dict_list.append({
                "dog_id": profile.dog_id,
                "user_id": profile.user_id,
                "dog_code": profile.dog_code,
                "dog_name": profile.dog_name,
                "birthday": profile.birthday,
                "weight": profile.weight,
                "height": profile.height,
                "photo": profile.photo,
                "gender": profile.memo
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json

def historyselect(mymodel, dog_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.dog_id == dog_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for history_tbl in result:
            result_dict_list.append({
                "user_id": history_tbl.user_id,
                "dog_id": history_tbl.dog_id,
                "date": str(history_tbl.date),
                "training_stroll": history_tbl.training_stroll,
                "sound_id": history_tbl.sound_id,
                "mood": history_tbl.mood,
                "title": history_tbl.title
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def soundselect(mymodel, sound_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.sound_id == sound_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for music_tbl in result:
            result_dict_list.append({
                "sound_id": music_tbl.sound_id,
                "user_id": music_tbl.user_id,
                "dog_id": music_tbl.dog_id,
                "music_type_code": music_tbl.music_type_code,
                "music_data": str(music_tbl.music_data),
                "title": music_tbl.title,
                "duration": str(music_tbl.duration),
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselect(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for customer_info in result:
            result_dict_list.append({
                "customer_id": customer_info.customer_id,
                "customer_name": customer_info.customer_name,
                "age": customer_info.age,
                "gender": customer_info.gender
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json


def myselectAll(mymodel):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = select(mymodel)
    try:
        # トランザクションを開始
        with session.begin():
            df = pd.read_sql_query(query, con=engine)
            result_json = df.to_json(orient='records', force_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        result_json = None

    # セッションを閉じる
    session.close()
    return result_json


def myupdate(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    customer_id = values.pop("customer_id")

    # query = "お見事！E0002の原因はこのクエリの実装ミスです。正しく実装しましょう"
    query = update(mymodel).values(values).where(mymodel.customer_id == customer_id)
    
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()
    # セッションを閉じる
    session.close()
    return "put"

def mydelete(mymodel, customer_id):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = delete(mymodel).where(mymodel.customer_id == customer_id)
    try:
        # トランザクションを開始
        with session.begin():
            result = session.execute(query)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return customer_id + " is deleted"