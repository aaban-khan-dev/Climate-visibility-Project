import sys
import os
import numpy as np
from pymongo import MongoClient
import pandas as pd
from zipfile import Path
from src.constant import *
from src.exception import VisibilityException
from src.logger import logging
from dataclasses import dataclass
from src.utils.main_utils import MainUtils
from src.data_access.visibility_data import VisibilityData

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str = os.path.join("artifact_folder","data_ingestion")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.main_utils = MainUtils()

    def export_collection_as_dataframe(self,collection_name:str,db_name:str):
        try:
            mongoclient = MongoClient(os.getenv("MONGODB_URL"))
            collection = mongoclient[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"],axis = 1)

            df.replace({"na":np.nan},inplace = True)

            return df
        
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    def export_data_into_raw_data_dir(self)->pd.DataFrame:
        """

        Method Name : export_data_into_feature_store
        Description : this methods reads data from mongoDB and stores it into Artifacts
        Output : dataset is returned as pd.DataFrame
        On Failure : write exception log and raise exception
        version : 0.1

        """
        try:
            logging.info("Exporting data from MongoDB to DataFrame")
            raw_batch_file_path = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(raw_batch_file_path,exist_ok = True)

            visibility_data = VisibilityData(
                database_name = MONGO_DATABASE_NAME
            )

            logging.info(f"Saving exported data into feature store file path : {raw_batch_file_path}")
            for collection_name,dataset in visibility_data.export_collection_as_dataframe():

                logging.info(f"shape of collection {collection_name} is {dataset.shape}")
                feature_store_file_path = os.path.join(raw_batch_file_path,collection_name + ".csv")
                dataset.to_csv(feature_store_file_path,index = False,header = True)

        except Exception as e:
            raise VisibilityException(e,sys) from e
    
    def initiate_data_ingestion(self):
        """
        Method Name : initiate_data_ingestion
        Description : this method initiates the data ingestion components of training pipeline
        Output : train set and test set are return as an artifacts of data ingestion component
        On Failure : write exception log and raise exception
        Version : 1.2
        Revision : Move setup to cloud

        """

        logging.info("Initiating data ingestion component of training pipeline")

        try:
            self.export_data_into_raw_data_dir()
            logging.info("Got the data from MongoDB")

            logging.info("Exited the data ingestion component of training pipeline")

            return self.data_ingestion_config.data_ingestion_dir
        
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
        

    