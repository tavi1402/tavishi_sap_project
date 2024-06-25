import logging
from src.exception import CustomException
import sys
from scipy.stats import ks_2samp
from dataclasses import dataclass
import os

@dataclass
class DataDriftArtifacts:
    drift_Report: str  = os.path.join("artifacts","data_drift","drift_report.json")

class DataDrift:
    def __init__(self,base_df,current_df) -> None:
        self.base_df=base_df
        self.current_df=current_df
        self.validation_error=dict()
        os.makedirs(os.path.join("artifacts","data_drift"),exist_ok=True)


    def data_drift(self,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = self.base_df.columns
            current_columns = self.current_df.columns

            for base_column in base_columns:
                base_data,current_data =self.base_df[base_column],self.current_df[base_column]
                #Null hypothesis is that both column data drawn from same distrubtion
                
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)
                print(same_distribution.pvalue)
                if same_distribution.pvalue>0.05:
                    #We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
            self.validation_error[report_key_name]=drift_report
            return self.validation_error
        except Exception as e:
            raise CustomException(e, sys)