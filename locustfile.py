from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def make_prediction(self):
        self.client.post("/predict", data={
            'Client_Income': '50000',
            'Car_Owned': '1',
            'Active_Loan': '0',
            'House_Own': '1',
            'Credit_Amount': '200000',
            'Loan_Annuity': '15000',
            'Client_Income_Type': 'Working',
            'Client_Education': 'Higher education',
            'Client_Marital_Status': 'Married',
            'Client_Gender': 'M',
            'Loan_Contract_Type': 'Revolving loans',
            'Client_Housing_Type': 'House / apartment',
            'Population_Region_Relative': '0.02',
            'Age_Days': '12000',
            'Employed_Days': '2000',
            'Registration_Days': '4000',
            'ID_Days': '1000',
            'Homephone_Tag': '1',
            'Workphone_Working': '1',
            'Client_Occupation': 'Managers',
            'Client_Family_Members': '2',
            'Cleint_City_Rating': '3',
            'Client_Permanent_Match_Tag': '1',
            'Client_Contact_Work_Tag': '1',
            'Type_Organization': 'Business Entity Type 3',
            'Score_Source_2': '0.5',
            'Score_Source_3': '0.3',
            'Phone_Change': '0.1',
            'Credit_Bureau': '1'
        })

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Simulate user waiting between 1 to 5 seconds between tasks
    host = "http://127.0.0.1:5001"  # Specify the base host to match Flask app

# if __name__ == "__main__":
#     import os
#     os.system("locust -f locustfile.py")  # Ensure to name this script locustfile.py for ease of use
