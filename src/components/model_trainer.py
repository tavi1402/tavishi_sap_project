import os
import sys
from dataclasses import dataclass

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, recall_score
import json
from src.logger import logging
from src.exception import CustomException

from src.utils import save_object, evaluate_model
import mlflow
from mlflow.tracking import MlflowClient

def slack_alerts():
    pass

client = MlflowClient(tracking_uri="http://34.30.89.156:5000")
remote_Server_Uri = "http://34.30.89.156:5000"
mlflow.set_tracking_uri(remote_Server_Uri)
mlflow.set_experiment("load_default_experiments")

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","trained_model", "model.pkl")
    output_json_accuracy= os.path.join("artifacts","trained_model", "output.json")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, X_train, X_test, y_train, y_test):
        try:
            with mlflow.start_run():
                models = {
                    "Logistic Regression": LogisticRegression(n_jobs=6),
                    "NaiveBayes Classifier": BernoulliNB(),
                    "DecisionTree Classifier": DecisionTreeClassifier(max_depth=15),
                    "RandomForest Classifier": RandomForestClassifier(n_jobs=6, max_depth=17),
                    "LGBM Classifier": LGBMClassifier(n_estimators=200, n_jobs=6, max_depth=15, num_leaves=256, verbosity=0),
                    "XGB Classifier": XGBClassifier(n_estimators=200, n_jobs=6, max_depth=15)
                }

                # Log specific parameters for models that have them
                mlflow.log_param("decisiontree_classifier_max_depth", 15)
                mlflow.log_param("randomforest_classifier_max_depth", 17)
                mlflow.log_param("lgbm_classifier_n_estimators", 200)
                mlflow.log_param("lgbm_classifier_max_depth", 15)
                mlflow.log_param("lgbm_classifier_num_leaves", 256)
                mlflow.log_param("xgb_classifier_n_estimators", 200)
                mlflow.log_param("xgb_classifier_max_depth", 15)

                logging.info("Starting Model Training")
                
                model_report: dict = evaluate_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models)

                # Get the best model based on recall score
                best_model_recall_score = max(model_report.values())

                # Get the best model's name
                best_model_name = [name for name, score in model_report.items() if score == best_model_recall_score][0]
                best_model = models[best_model_name]

                logging.info("Model Training completed")
                
                if best_model_recall_score < 0.4:
                    logging.info("No best model found")
                    slack_alerts()
                    return {"status":"false","message":"accuracy is worst...."}
                else:
                    save_object(
                        file_path=self.model_trainer_config.trained_model_file_path,
                        obj=best_model
                    )

                    logging.info(f"Best model: {best_model_name}")

                    y_pred = best_model.predict(X_test)
                    acc = accuracy_score(y_test, y_pred)
                    recall = recall_score(y_test, y_pred)

                    mlflow.log_metric("accuracy", acc)
                    mlflow.log_metric("recall", recall)
                    mlflow.log_param("best_model", best_model_name)
                    logging.info(f"Accuracy: {acc}")
                    logging.info(f"Recall: {recall}")
                    output={"accuract":acc,"recall":recall,"best_model_name":best_model_name}
                    json.dump(output,open(self.model_trainer_config.output_json_accuracy,"w"))
                    return {"status":"true","output":self.model_trainer_config.trained_model_file_path}
        except Exception as e:
            print(str(CustomException(e,sys)))
            return {"status":"false","output":str(CustomException(e,sys))}
