import os
import sys
from dataclasses import dataclass

import json

import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, RobustScaler
from src.components import data_drift
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"data_transformation", 'preprocessor.pkl')
    train_data_path: str=os.path.join('artifacts',"data_transformation", 'train.csv')
    test_data_path: str=os.path.join('artifacts', "data_transformation",'test.csv')
    label_encodings_path: str=os.path.join('artifacts',"data_transformation", 'label_encodings.json')

class DataTransformation:
    def __init__(self,raw_data_path: os.PathLike,base_data_path: os.PathLike):
        os.makedirs(os.path.join('artifacts',"data_transformation"),exist_ok=True)
        self.raw_data_path=raw_data_path
        self.base_data_path=base_data_path
        self.data_transformation_config = DataTransformationConfig()

    
    def get_data_transformer_object(self, numeric_cols, one_hot_enc_cols):
        '''
        This function is responsible for creatubg the data preprocessor object
        '''
        try:
            numeric_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', RobustScaler())
            ])

            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder', OneHotEncoder())
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('numeric_pipeline', numeric_pipeline, numeric_cols),
                    ('categorical_pipeline', categorical_pipeline, one_hot_enc_cols)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self):

        try:
            df_raw = pd.read_csv(self.raw_data_path)

            logging.info("Completed reading the raw data for further preprocessing")

            logging.info("Starting Preprocessing")

            df_raw.drop(columns = ['ID','Application_Process_Day','Application_Process_Hour', 'Mobile_Tag', 'Accompany_Client'], inplace=True)
            def replace_unwanted_chars(value):
                if isinstance(value, str):
                    return re.sub(r'[$@&]', '', value)
                return value

            df_raw = df_raw.applymap(replace_unwanted_chars)
            potential_numerical_columns = ['Client_Income', 'Credit_Amount', 'Loan_Annuity', 'Population_Region_Relative',
                                           'Age_Days', 'Employed_Days', 'Registration_Days', 'ID_Days', 'Score_Source_3']

            for col in potential_numerical_columns:
                df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
            
            potential_categorical_columns = ['Car_Owned', 'Bike_Owned', 'Active_Loan', 'House_Own', 'Homephone_Tag', 'Workphone_Working']

            for col in potential_categorical_columns:
                df_raw[col] = df_raw[col].replace({1: 'Yes', 0: 'No'})


            def map_income_type(category):
                if category in ['Student', 'Unemployed', 'Maternity leave', 'Businessman']:
                    return 'Other'
                else:
                    return category

            df_raw['Client_Income_Type'] = df_raw['Client_Income_Type'].apply(map_income_type)
            def map_occupation(category):
                if pd.isna(category):
                    return 'Unknown'
                elif category in ['Sales', 'Realty agents', 'Managers', 'Accountants', 'High skill tech', 'IT']:
                    return 'Professional'
                elif category in ['Laborers', 'Core', 'Drivers', 'Cleaning', 'Low-skill Laborers']:
                    return 'Skilled Labor'
                elif category in ['HR', 'Waiters/barmen', 'Cooking', 'Private service', 'Security', 'Secretaries']:
                    return 'Service'
                elif category == 'Medicine':
                    return 'Healthcare'
                else:
                    return 'Other'

            df_raw['Client_Occupation'] = df_raw['Client_Occupation'].apply(map_occupation)

            def map_organization(category):
                if pd.isna(category):
                    return 'Unknown'
                elif category == 'XNA':
                    return 'Unknown'
                elif category in ['Self-employed', 'Government']:
                    return 'Public Sector'
                elif category in ['Business Entity Type 3', 'Business Entity Type 2', 'Business Entity Type 1', 'Construction']:
                    return 'Business'
                elif category in ['Trade: type 3', 'Trade: type 7', 'Trade: type 2', 'Agriculture']:
                    return 'Trade'
                elif category in ['Military', 'Medicine', 'Housing', 'Industry: type 1', 'Industry: type 11', 'Bank', 'School', 'Industry: type 9', 'Postal', 'University']:
                    return 'Institution'
                elif category in ['Transport: type 4', 'Transport: type 2', 'Transport: type 3', 'Transport: type 1']:
                    return 'Transport'
                else:
                    return 'Other'

            df_raw['Type_Organization'] = df_raw['Type_Organization'].apply(map_organization)

            df_raw['Client_Gender'].replace('XNA', df_raw['Client_Gender'].mode().iloc[0], inplace=True)

            percent_missing = (df_raw.isnull().sum() / len(df_raw)) * 100

            columns_to_drop = percent_missing[percent_missing > 25].index

            df_raw.drop(columns=columns_to_drop, inplace=True)

            def handle_outliers(df):

                def cap_outliers(series, lower_bound, upper_bound):
                    series = np.where(series > upper_bound, upper_bound, series)
                    # series = np.where(series < lower_bound, lower_bound, series)
                    return series

                columns_to_cap = ['Population_Region_Relative', 'Score_Source_2']

                for column in columns_to_cap:
                    Q1 = df[column].quantile(0.25)
                    Q3 = df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    df[column] = cap_outliers(df[column], lower_bound, upper_bound)


                columns_to_filter = ['Employed_Days']

                for column in columns_to_filter:
                    Q1 = df[column].quantile(0.25)
                    Q3 = df[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

                return df

            df_raw = handle_outliers(df_raw)


            columns_to_drop = ['Child_Count', 'Bike_Owned']

            df_raw.drop(columns=columns_to_drop, inplace=True)



            X = df_raw.drop('Default', axis=1)
            y = df_raw['Default']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, stratify=y, random_state=42)
            numeric_cols = X_train.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

            print(f"\nNum cols: {len(numeric_cols), numeric_cols},\n\nCat cols: {len(categorical_cols), categorical_cols}")

            label_enc_cols = []
            one_hot_enc_cols = []

            for col in categorical_cols:
                if len(X_train[col].value_counts()) > 2:
                    label_enc_cols.append(col)
                else:
                    one_hot_enc_cols.append(col)

            imputer = SimpleImputer(strategy='most_frequent')
            X_train[label_enc_cols] = imputer.fit_transform(X_train[label_enc_cols])
            X_test[label_enc_cols] = imputer.transform(X_test[label_enc_cols])

            label_encoders = {}
            label_mappings = {}
            for col in label_enc_cols:
                le = LabelEncoder()
                X_train[col] = le.fit_transform(X_train[col])
                X_test[col] = le.transform(X_test[col])
                label_encoders[col] = le
                label_mappings[col] = {class_: int(index) for index, class_ in enumerate(le.classes_)}


            with open(self.data_transformation_config.label_encodings_path, 'w') as f:
                json.dump(label_mappings, f, indent=4)

            preprocessing_obj = self.get_data_transformer_object(numeric_cols, one_hot_enc_cols)


            X_train_transformed = preprocessing_obj.fit_transform(X_train)
            X_test_transformed = preprocessing_obj.transform(X_test)
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            logging.info("Saved preprocessing object")

            logging.info("Resampling imbalanced data")

            smote = SMOTE(random_state=42)
            X_train_smote, y_train_smote = smote.fit_resample(X_train_transformed, y_train)
            logging.info("Saving train and test data")


            train_data = pd.concat([pd.DataFrame(X_train_smote), pd.DataFrame(y_train_smote)], axis=1)
            drift_report_=data_drift.DataDrift(base_df=train_data,current_df=train_data).data_drift("train_drift")
            json.dump(drift_report_,open(data_drift.DataDriftArtifacts.drift_Report,"w"))
            train_data.to_csv(self.data_transformation_config.train_data_path, index=False)

            test_data = pd.concat([pd.DataFrame(X_test_transformed), pd.DataFrame(y_test)], axis=1)
            # drift_report=data_drift.DataDrift(base_df=test_data,current_df=test_data).data_drift("test_drift")
            # drift_report_["test_drift"]=drift_report
            # json.dump(drift_report_,open(data_drift.DataDriftArtifacts.drift_Report,"w"))
            test_data.to_csv(self.data_transformation_config.test_data_path, index=False)


            return {"status":"true","output":(
                X_train_smote,
                X_test_transformed,
                y_train_smote,
                y_test
            ),"preprocessor_file_path":self.data_transformation_config.preprocessor_obj_file_path}
        except Exception as e:
            return {"status":"false","output":str(CustomException(e, sys))}
