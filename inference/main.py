import pandas as pd
from prediction_pipeline import PredictPipeline, CustomData

def main():
    # Create an instance of CustomData with sample data
    custom_data = CustomData(
        Client_Income=50000,
        Car_Owned='Yes',
        Active_Loan='No',
        House_Own='Yes',
        Credit_Amount=200000,
        Loan_Annuity=15000,
        Client_Income_Type='Working',
        Client_Education='Higher Education',
        Client_Marital_Status='Married',
        Client_Gender='Male',
        Loan_Contract_Type='Cash loans',
        Client_Housing_Type='House / apartment',
        Population_Region_Relative=0.02,
        Age_Days=12000,
        Employed_Days=4000,
        Registration_Days=2000,
        ID_Days=1500,
        Homephone_Tag='No',
        Workphone_Working='Yes',
        Client_Occupation='Manager',
        Client_Family_Members=3,
        Cleint_City_Rating=2,
        Client_Permanent_Match_Tag='Yes',
        Client_Contact_Work_Tag='No',
        Type_Organization='Business Entity Type 3',
        Score_Source_2=0.5,
        Score_Source_3=0.3,
        Phone_Change=1,
        Credit_Bureau=2
    )

    # Get the data as a dataframe
    df, custom_data_dict = custom_data.get_data_as_dataframe()

    # Create an instance of PredictPipeline and make predictions
    pipeline = PredictPipeline()
    predictions = pipeline.predict(df)

    print(f"Predictions: {predictions}")

if __name__ == "__main__":
    main()
