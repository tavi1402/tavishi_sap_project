from src.exception import CustomException
from loguru import logger as logging
import sys
from src.utils import upload_model_to_gcs
import os


class ModelPusher(object):
    def __init__(self, model_dir_path=None,model_type="ml_model",model_name="model"):
        try:
            logging.info(f"{'>>>'*20} Model Pusher {'<<<'*20}")
            self.dir = model_dir_path
            self.model_type=model_type
            self.model_name=model_name
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_model_pusher(self):
        try:
            logging.info("Model Pusher is initiated")
            if self.model_type=="preprocessor":
                self.upload()
            elif self.model_type=="ml_model":
                self.upload()
        except Exception as e:
            raise CustomException(e, sys)

    def upload(self):
        model_saved_dir = self.dir
        bucket_name = os.getenv("GCS_BUCKET")
        if not bucket_name:
            raise ValueError("GCS_BUCKET environment variable is not set.")
        model_version = upload_model_to_gcs(bucket_name=bucket_name, model_path=model_saved_dir,type=self.model_type,model_name=self.model_name)
        logging.info(f"Model uploaded to GCS with version {model_version}")
