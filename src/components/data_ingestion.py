import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass
from src.utils import get_collection_as_dataframe


@dataclass
class DataIngestionConfig:
    raw_data_path: str=os.path.join('artifacts',"data_ingestion", 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiated Data Ingestion")
        try:
            if os.path.exists(self.ingestion_config.raw_data_path):
                return {"status":"true","output":self.ingestion_config.raw_data_path}
            df:pd.DataFrame  = get_collection_as_dataframe(
                database_name=os.getenv("DATABASE_NAME"), 
                collection_name=os.getenv("COLLECTION_NAME"))
            
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Data Ingestion completed")
            return {"status":"true","output":self.ingestion_config.raw_data_path}

        except Exception as e:
            return {"status":"false","error_message": str(CustomException(e, sys))}
        
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    result = data_ingestion.initiate_data_ingestion()
    if result["status"] == "true":
        logging.info(f"Data ingestion successful. Data saved to: {result['output']}")
    else:
        logging.error(f"Data ingestion failed with error: {result['error_message']}")
