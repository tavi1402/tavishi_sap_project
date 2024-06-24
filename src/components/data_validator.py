import os

try:
    import great_expectations as ge
    os.system("great_expectations init")
    import logging
    import json
    from great_expectations.data_context.types.base import (
    DataContextConfig,
    DatasourceConfig,
    FilesystemStoreBackendDefaults,
)
    from great_expectations.core.batch import RuntimeBatchRequest
    from great_expectations.data_context import BaseDataContext

except ModuleNotFoundError:
    os.system("pip install great_expectations")
    os.system("great_expectations init")
from dataclasses import dataclass

@dataclass
class DataValidationArtifact:
    data_validation_res=os.path.join("artifacts","data_validation","res.json")

class DataValidation(object):
    def __init__(self,data_path):
        self.data_validation_artifact=DataValidationArtifact()
        os.makedirs(os.path.join("artifacts","data_validation"),exist_ok=True)
        logging.info("DATA VALIDATION STARTED")
        self.data_path=data_path
        self.data_read_=ge.read_csv(self.data_path)
        self.data_read=ge.from_pandas(self.data_read_)

    def validate_data(self):
        logging.info("expectation suite started to validate")
        #validate the data
        self.data_read.expect_column_values_to_be_unique("ID")

        # self.data_read.expect_column_values_to_be_of_type("Client_Income", "str")

        # self.data_read.expect_column_values_to_be_in_set("Car_Owned", [0, 1])
        # self.data_read.expect_column_values_to_be_in_set("Bike_Owned", [0, 1])

        # self.data_read.expect_column_values_to_be_in_set("Active_Loan", [0, 1])
        # self.data_read.expect_column_values_to_be_in_set("House_Own", [0, 1])

        # self.data_read.expect_column_values_to_be_of_type("Child_Count", "int")

        # self.data_read.expect_column_values_to_be_of_type("Credit_Amount", "str")
        # self.data_read.expect_column_values_to_be_of_type("Loan_Annuity", "str")

        # self.data_read.expect_column_values_to_not_be_null("Accompany_Client")

        # self.data_read.expect_column_values_to_not_be_null("Client_Income_Type")

        # self.data_read.expect_column_values_to_not_be_null("Client_Education")
        # self.data_read.expect_column_values_to_be_in_set("Client_Marital_Status", ["D", "S", "M", "W"])
        # self.data_read.expect_column_values_to_be_in_set("Client_Gender", ["M", "F"])
        # self.data_read.expect_column_values_to_be_in_set("Loan_Contract_Type", ["CL", "RL"])

        # self.data_read.expect_column_values_to_not_be_null("Client_Housing_Type")

        # self.data_read.expect_column_values_to_be_of_type("Population_Region_Relative", "float")
        # self.data_read.expect_column_values_to_be_of_type("Age_Days", "int")
        # self.data_read.expect_column_values_to_be_of_type("Employed_Days", "int")
        # self.data_read.expect_column_values_to_be_of_type("Registration_Days", "int")
        # self.data_read.expect_column_values_to_be_of_type("ID_Days", "int")
        # self.data_read.expect_column_values_to_be_of_type("Own_House_Age", "str")
        # self.data_read.expect_column_values_to_be_in_set("Mobile_Tag", [0, 1])
        # self.data_read.expect_column_values_to_be_in_set("Homephone_Tag", [0, 1])

        # self.data_read.expect_column_values_to_be_in_set("Workphone_Working", [0, 1])
        # self.data_read.expect_column_values_to_not_be_null("Client_Occupation")
        # self.data_read.expect_column_values_to_be_of_type("Client_Family_Members", "int")

        # self.data_read.expect_column_values_to_be_in_set("Cleint_City_Rating", [1, 2, 3])
        # self.data_read.expect_column_values_to_be_in_set("Application_Process_Day", [0, 1, 2, 3, 4, 5, 6])

        # self.data_read.expect_column_values_to_be_of_type("Application_Process_Hour", "int")
        # self.data_read.expect_column_values_to_be_in_set("Client_Permanent_Match_Tag", [0, 1])

        # self.data_read.expect_column_values_to_be_in_set("Client_Contact_Work_Tag", [0, 1])

        # self.data_read.expect_column_values_to_not_be_null("Type_Organization")
        # self.data_read.expect_column_values_to_be_of_type("Score_Source_1", "float")
        # self.data_read.expect_column_values_to_be_of_type("Score_Source_2", "float")
        # self.data_read.expect_column_values_to_be_of_type("Score_Source_3", "float")
        # self.data_read.expect_column_values_to_be_of_type("Social_Circle_Default", "int")
        # self.data_read.expect_column_values_to_be_of_type("Phone_Change", "int")
        # self.data_read.expect_column_values_to_be_of_type("Credit_Bureau", "int")
        # self.data_read.expect_column_values_to_be_in_set("Default", [0, 1])
        # Save the expectation suite

        data_context_config = DataContextConfig(
        datasources={
            "loan_default_datasource": DatasourceConfig(
                class_name="Datasource",
                module_name="great_expectations.datasource",
                execution_engine={
                    "class_name": "PandasExecutionEngine",
                    "module_name": "great_expectations.execution_engine",
                },
                data_connectors={
                    "default_runtime_data_connector_name": {
                        "class_name": "RuntimeDataConnector",
                        "batch_identifiers": ["default_identifier_name"],
                    }
                },
            )
        },
        store_backend_defaults=FilesystemStoreBackendDefaults(
            root_directory=f"{os.getcwd()}/gx"
            ),
        )

        def get_batch_request(df):
            os.makedirs("gx_suite", exist_ok=True)
            batch_request = RuntimeBatchRequest(
                datasource_name="loan_default_datasource",
                data_connector_name="default_runtime_data_connector_name",
                data_asset_name="loan_default_Batch_Asset",  # This can be anything that identifies this data_asset for you
                runtime_parameters={"batch_data": df},  # df is your dataframe
                batch_identifiers={"default_identifier_name": "default_identifier"},
            )
            return batch_request
        context = BaseDataContext(project_config=data_context_config)
        context.save_expectation_suite(
            expectation_suite_name="loan_default_expectation_suite",
            expectation_suite=self.data_read.get_expectation_suite(
                discard_failed_expectations=False
            ),
        )
        context.build_data_docs()
        batch_request = get_batch_request(self.data_read_)

        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite=self.data_read.get_expectation_suite(
                discard_failed_expectations=False
            ),
        )
        results = validator.validate(catch_exceptions=True).to_json_dict()
        json.dump(results,open(self.data_validation_artifact.data_validation_res,"w"))
        logging.info(f"expectation suite ended with status {results['success']}")
        if results['success']==True:
            return {"status":"true","output":self.data_path}
        return {"status":"false","output":"Please check the data validation results"}
    