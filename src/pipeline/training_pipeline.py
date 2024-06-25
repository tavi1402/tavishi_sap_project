import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
load_dotenv()

from src.components.data_ingestion import DataIngestion
from src.components.data_validator import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_pusher import ModelPusher


def run_training_pipeline():
    data_ingestion = DataIngestion()
    data_ingestion_status = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_status)
    if data_ingestion_status["status"]=="true":
        data_validation = DataValidation(data_path=data_ingestion_status["output"])
        data_validation_status=data_validation.validate_data()
        print(data_validation_status)
        if data_validation_status["status"]=="true":
            data_transformation=DataTransformation(raw_data_path=data_validation_status["output"],base_data_path="Dataset.csv")
            data_transformation_status = data_transformation.initiate_data_transformation()
            print(data_transformation_status)
            if data_transformation_status["status"]=="true":
                model_trainer = ModelTrainer()
                X_train, X_test, y_train, y_test=data_transformation_status["output"]
                model_trainer_Status=model_trainer.initiate_model_trainer(X_train, X_test, y_train, y_test)

                if model_trainer_Status["status"] == "true":
                    model_pusher=ModelPusher("artifacts\\trained_model","ml_model","model")
                    preprocess_pkl_pusher=ModelPusher("artifacts\\data_transformation","preprocessor","preprocessor")
                    preprocess_pkl_pusher.initiate_model_pusher()
                    result=model_pusher.initiate_model_pusher()
                    return result
                else:
                    return {"status":"false"}

if __name__=="__main__":
    run_training_pipeline()
