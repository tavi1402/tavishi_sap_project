import sys

import pandas as pd

import json

from src.exception import CustomException
from src.utils import load_object
import functools
import os 


class PredictPipeline:
    def __init__(self):
        pass

    @functools.lru_cache()
    def load_model(self):
        model_path = "artifacts/model.pkl"
        preprocessor_path = "artifacts/preprocessor.pkl"
        # model_path = "models/ml_model/final-model.pkl"
        # preprocessor_path = "models/preprocessor/preprocessor.pkl"
        model = load_object(file_path=model_path)
        preprocessor = load_object(file_path=preprocessor_path)
        return model,preprocessor
    
    def predict(self, features):
        try:
            model,preprocessor=self.load_model()
            with open("artifacts/label_encodings.json", "r") as f:
                label_encodings = json.load(f)

            features_mapped = {
                "Client_Income_Type": [label_encodings["Client_Income_Type"].get(features["Client_Income_Type"].iloc[0], 2)],
                "Client_Education": [label_encodings["Client_Education"].get(features["Client_Education"].iloc[0], 0)],
                "Client_Marital_Status": [label_encodings["Client_Marital_Status"].get(features["Client_Marital_Status"].iloc[0], 2)],
                "Client_Housing_Type": [label_encodings["Client_Housing_Type"].get(features["Client_Housing_Type"].iloc[0], 1)],
                "Client_Occupation": [label_encodings["Client_Occupation"].get(features["Client_Occupation"].iloc[0], 4)],
                "Type_Organization": [label_encodings["Type_Organization"].get(features["Type_Organization"].iloc[0], 6)],
                }

            features.update(features_mapped)
            print(features)
            data_scaled = preprocessor.transform(features)
            predictions = model.predict(data_scaled)
        
            return predictions
        
        except Exception as e:
            raise CustomException(e, sys)

# Class to map inputs given to HTML with backend
class CustomData:
    def __init__(self,
        Client_Income: float,
        Car_Owned: str,
        Active_Loan: str,
        House_Own: str,
        Credit_Amount: float,
        Loan_Annuity: float,
        Client_Income_Type: str,
        Client_Education: str,
        Client_Marital_Status: str,
        Client_Gender: str,
        Loan_Contract_Type: str,
        Client_Housing_Type: str,
        Population_Region_Relative: float,
        Age_Days: int,
        Employed_Days: int,
        Registration_Days: int,
        ID_Days: int,
        Homephone_Tag: str,
        Workphone_Working: str,
        Client_Occupation: str,
        Client_Family_Members: int,
        Cleint_City_Rating: int,
        Client_Permanent_Match_Tag: str,
        Client_Contact_Work_Tag: str,
        Type_Organization: str,
        Score_Source_2: float,
        Score_Source_3: float,
        Phone_Change: int,
        Credit_Bureau: int,
    ):

        self.Client_Income = Client_Income
        self.Car_Owned = Car_Owned
        self.Active_Loan = Active_Loan
        self.House_Own = House_Own
        self.Credit_Amount = Credit_Amount
        self.Loan_Annuity = Loan_Annuity
        self.Client_Income_Type = Client_Income_Type
        self.Client_Education = Client_Education
        self.Client_Marital_Status = Client_Marital_Status
        self.Client_Gender = Client_Gender
        self.Loan_Contract_Type = Loan_Contract_Type
        self.Client_Housing_Type = Client_Housing_Type
        self.Population_Region_Relative = Population_Region_Relative
        self.Age_Days = Age_Days
        self.Employed_Days = Employed_Days
        self.Registration_Days = Registration_Days
        self.ID_Days = ID_Days
        self.Homephone_Tag = Homephone_Tag
        self.Workphone_Working = Workphone_Working
        self.Client_Occupation = Client_Occupation
        self.Client_Family_Members = Client_Family_Members
        self.Cleint_City_Rating = Cleint_City_Rating
        self.Client_Permanent_Match_Tag = Client_Permanent_Match_Tag
        self.Client_Contact_Work_Tag = Client_Contact_Work_Tag
        self.Type_Organization = Type_Organization
        self.Score_Source_2 = Score_Source_2
        self.Score_Source_3 = Score_Source_3
        self.Phone_Change = Phone_Change
        self.Credit_Bureau = Credit_Bureau


    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "Client_Income": [self.Client_Income],
                "Car_Owned": [self.Car_Owned],
                "Active_Loan": [self.Active_Loan],
                "House_Own": [self.House_Own],
                "Credit_Amount": [self.Credit_Amount],
                "Loan_Annuity": [self.Loan_Annuity],
                "Client_Income_Type": [self.Client_Income_Type],
                "Client_Education": [self.Client_Education],
                "Client_Marital_Status": [self.Client_Marital_Status],
                "Client_Gender": [self.Client_Gender],
                "Loan_Contract_Type": [self.Loan_Contract_Type],
                "Client_Housing_Type": [self.Client_Housing_Type],
                "Population_Region_Relative": [self.Population_Region_Relative],
                "Age_Days": [self.Age_Days],
                "Employed_Days": [self.Employed_Days],
                "Registration_Days": [self.Registration_Days],
                "ID_Days": [self.ID_Days],
                "Homephone_Tag": [self.Homephone_Tag],
                "Workphone_Working": [self.Workphone_Working],
                "Client_Occupation": [self.Client_Occupation],
                "Client_Family_Members": [self.Client_Family_Members],
                "Cleint_City_Rating": [self.Cleint_City_Rating],
                "Client_Permanent_Match_Tag": [self.Client_Permanent_Match_Tag],
                "Client_Contact_Work_Tag": [self.Client_Contact_Work_Tag],
                "Type_Organization": [self.Type_Organization],
                "Score_Source_2": [self.Score_Source_2],
                "Score_Source_3": [self.Score_Source_3],
                "Phone_Change": [self.Phone_Change],
                "Credit_Bureau": [self.Credit_Bureau],
            }

            return pd.DataFrame(custom_data_input_dict),custom_data_input_dict

        except Exception as e:
            raise CustomException(e, sys)