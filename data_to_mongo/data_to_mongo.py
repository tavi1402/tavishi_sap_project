import pandas as pd
import json 
from dotenv import load_dotenv
load_dotenv()
from utils import *

if __name__=="__main__":
    df=pd.read_csv(env.data_file_path)
    print(f"Rows and columns in the data file: {df.shape}")
    df.reset_index(drop=True,inplace=True)
    json_records=list(json.loads(df.T.to_json()).values())
    print(json_records[0])
    client[env.database_name][env.collection_name].insert_many(json_records)
    print("Data uploaded to mongodb successfully")