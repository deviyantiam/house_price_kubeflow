import logging
import os
import uuid
import pandas as pd
import uvicorn
import pickle
import pytz
from typing import Dict
from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime
from module import task_manager

load_dotenv()

app = FastAPI()

class HousePriceModel:
    def __init__(self, name: str):
        self.logger = logging.getLogger('kserve')
        self.name = name
        self.ready = False
        self.model_path = os.getenv("MODEL")
        self.train_path = os.getenv("TRAIN_DF")
        self.conn = task_manager.create_connection(os.getcwd() + "/sqlitedb/tasks.sqlite3")
        self.load()

    def load(self):
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        self.ready = True

    def convert_columns_to_binary(self, df, columns_to_convert):
        for col in columns_to_convert:
            df[col] = df[col].map(lambda x: 1 if x == 'yes' else 0)
        return df

    def convert_furnish_column(self, df, type, categorical_column_list):
        if type == 'train':
            df = pd.get_dummies(df, drop_first=True, columns=categorical_column_list)
        else:
            df = pd.get_dummies(df, drop_first=False, columns=categorical_column_list)
        return df

    def predict_one(self, request: Dict):
        task_id = str(uuid.uuid4())
        task_name = "predict_house_price"
        jakarta_timezone = pytz.timezone('Asia/Jakarta')
        begin_date = datetime.now(jakarta_timezone)
        try:
            request_raw = {
                'area': [float(request["area"])],
                'bedrooms': [int(request["bedrooms"])],
                'bathrooms': [int(request["bathrooms"])],
                'stories': [int(request["stories"])],
                'mainroad': [str(request["mainroad"])],
                'guestroom': [str(request["guestroom"])],
                'basement': [str(request["basement"])],
                'hotwaterheating': [str(request["hotwaterheating"])],
                'airconditioning': [str(request["airconditioning"])],
                'parking': [int(request["parking"])],
                'prefarea': [str(request["prefarea"])],
                'furnishingstatus': [str(request["furnishingstatus"])]
            }
            data_to_predict = pd.DataFrame(request_raw)
            target = 'price'
            x_train = pd.read_csv(self.train_path).head().drop(columns=target)

            columns_to_convert_bool = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
            data_to_predict = self.convert_columns_to_binary(data_to_predict, columns_to_convert_bool)
            data_to_predict = self.convert_furnish_column(data_to_predict, 'test', ['furnishingstatus',])

            _, data_to_predict = x_train.align(data_to_predict, join='left', axis=1)
            data_to_predict.fillna(0,inplace=True)
            self.model.predict(data_to_predict)
            results = [{"status": "OK", "prediction": self.model.predict(data_to_predict)[0]}]
            
            status = "OK"
        except Exception as err:
            results = [{"status": "NOT OK/Error {}".format(str(err)), "prediction": 0}]
            status = "NOK"
        end_date = datetime.now(jakarta_timezone)
        
        task_manager.update_task(
            conn = self.conn,
            task_id = task_id,
            task_type = task_name,
            task_status = status,
            task_start_date = begin_date,
            task_end_date = end_date,
            messages=str(results),
            types="insert"
        )
        self.logger.info(f"results:-- {results}")
        return {"predictions": results}

model = HousePriceModel("house-price-rf")

@app.post("/predict/")
async def predict(request: Dict):
    return model.predict_one(request)

if __name__ == '__main__':
    tm_conn = task_manager.create_connection(os.getcwd() + "/sqlitedb/tasks.sqlite3")
    task_manager.create_table(tm_conn)
    uvicorn.run("app:app", host="0.0.0.0", port = 8000)