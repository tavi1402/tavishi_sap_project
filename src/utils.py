import os
import sys

import pickle

from sklearn.metrics import recall_score

from src.logger import logging
from src.exception import CustomException

import pandas as pd
import sys
from loguru import logger as logging
from src.exception import CustomException
import pymongo

import boto3

from google.cloud import storage
from datetime import datetime
import os

def upload_model_to_gcs(bucket_name="tavishi_sap_project", model_path=None,type=None,model_name=None):
    model_version = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    gcs_path = f"models/{type}/{model_name}_v{model_version}.pkl"
    local_model_path = f"{model_path}\{model_name}.pkl"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_model_path)
    return model_version


def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        logging.info(f'Exception occured during saving {obj} object')
        raise CustomException(e, sys)
    
def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(list(models))):

            # print(list(models.keys())[i])
            model = list(models.values())[i]
            
            # Train model
            model.fit(X_train, y_train)
            
            # Predict on Test data
            y_pred = model.predict(X_test)
            
            # accuracy = accuracy_score(y_test, y_pred)
            # precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            # f2_scr = fbeta_score(y_test, y_pred, beta=2)
            
            report[list(models.keys())[i]] =  recall

        return report
    
    except Exception as e:
            logging.info('Exception occured during model training')
            raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception occured in load_object function utils')
        raise CustomException(e,sys)
    

mongo_client=pymongo.MongoClient(os.getenv("MONGODB_CREDENTIALS"))

def get_collection_as_dataframe(database_name:str,collection_name:str):
    try:
        logging.info(f"Reading the data from the database from MongoDB --> database name-->[{database_name}] ,collection name-->[{collection_name}]")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Data loaded from MongoDB successfully with rows {df.shape[0]} and columns {df.shape[1]}")
        if "_id" in df.columns:
            logging.info("dropping the _id column")
            df.drop("_id",axis=1,inplace=True)
            logging.info("Dropped the _id column successfully")
        return df
    except Exception as e:
        raise CustomException(e,sys)
