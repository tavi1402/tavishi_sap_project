import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, render_template
from prediction_pipeline import CustomData, PredictPipeline
import logging
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client=pymongo.MongoClient(os.getenv("MONGODB_CREDENTIALS"))

import sentry_sdk

sentry_sdk.init(
    dsn="https://624dcc8ee1e847ac87e6cc9fdec3c7e8@o4505453528940544.ingest.us.sentry.io/4505453531299840",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        try:
            # Collect form data
            data = CustomData(
                Client_Income=request.form.get('Client_Income'),
                Car_Owned=request.form.get('Car_Owned'),
                Active_Loan=request.form.get('Active_Loan'),
                House_Own=request.form.get('House_Own'),
                Credit_Amount=request.form.get('Credit_Amount'),
                Loan_Annuity=request.form.get('Loan_Annuity'),
                Client_Income_Type=request.form.get('Client_Income_Type'),
                Client_Education=request.form.get('Client_Education'),
                Client_Marital_Status=request.form.get('Client_Marital_Status'),
                Client_Gender=request.form.get('Client_Gender'),
                Loan_Contract_Type=request.form.get('Loan_Contract_Type'),
                Client_Housing_Type=request.form.get('Client_Housing_Type'),
                Population_Region_Relative=request.form.get('Population_Region_Relative'),
                Age_Days=request.form.get('Age_Days'),
                Employed_Days=request.form.get('Employed_Days'),
                Registration_Days=request.form.get('Registration_Days'),
                ID_Days=request.form.get('ID_Days'),
                Homephone_Tag=request.form.get('Homephone_Tag'),
                Workphone_Working=request.form.get('Workphone_Working'),
                Client_Occupation=request.form.get('Client_Occupation'),
                Client_Family_Members=request.form.get('Client_Family_Members'),
                Cleint_City_Rating=request.form.get('Cleint_City_Rating'),
                Client_Permanent_Match_Tag=request.form.get('Client_Permanent_Match_Tag'),
                Client_Contact_Work_Tag=request.form.get('Client_Contact_Work_Tag'),
                Type_Organization=request.form.get('Type_Organization'),
                Score_Source_2=request.form.get('Score_Source_2'),
                Score_Source_3=request.form.get('Score_Source_3'),
                Phone_Change=request.form.get('Phone_Change'),
                Credit_Bureau=request.form.get('Credit_Bureau')
            )

            # Convert to DataFrame
            pred_df,custom_data_input_dict = data.get_data_as_dataframe()
            client["mlops"]["web_data"].insert_one(custom_data_input_dict)

            # Replace empty strings with None
            columns_to_check = ['Client_Income', 'Credit_Amount', 'Loan_Annuity', 'Population_Region_Relative',
                                'Age_Days', 'Employed_Days', 'Registration_Days', 'ID_Days', 'Client_Family_Members',
                                'Cleint_City_Rating', 'Score_Source_2', 'Score_Source_3', 'Phone_Change', 'Credit_Bureau']

            for col in columns_to_check:
                pred_df[col] = pred_df[col].replace('', None)

            # Debug: Print the DataFrame
            logging.debug(pred_df)

            # Prediction
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            # Convert results to human-readable format
            results = ['No Default' if results[0] == 0 else 'Default']

            return render_template('index.html', results=results[0])

        except Exception as e:
            # Print the error to the console
            logging.error(f"Error occurred: {e}", exc_info=True)
            # Optionally, you can display a user-friendly error message
            return render_template('index.html', results="Error during prediction")

if __name__ == "__main__":
    app.run(debug=True)