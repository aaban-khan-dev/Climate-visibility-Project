import sys
import os
import numpy as np
from pymongo import MongoClient
import pandas as pd

from src.constant import *
from src.exception import VisibilityException
from src.logger import logging
from dataclasses import dataclass
from src.utils.main_utils import MainUtils
from datetime import datetime


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join("artifact_folder", "data_ingestion")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.main_utils = MainUtils()

    def export_collection_as_dataframe(self, collection_name: str, db_name: str):
        try:
            mongoclient = MongoClient(os.getenv("MONGODB_URL"))
            collection = mongoclient[db_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def export_data_into_raw_data_dir(self) -> pd.DataFrame:
        try:
            logging.info("Exporting data from MongoDB to DataFrame")

            raw_batch_file_path = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(raw_batch_file_path, exist_ok=True)

            df = self.export_collection_as_dataframe(
                collection_name=MONGO_COLLECTION_NAME,
                db_name=MONGO_DATABASE_NAME
            )

            logging.info(f"Dataset shape: {df.shape}")

            current_time = datetime.now()
            date_stamp = current_time.strftime("%d%m%Y")
            time_stamp = current_time.strftime("%H%M%S")

            file_name = f"visibility_{date_stamp}_{time_stamp}.csv"

            feature_store_file_path = os.path.join(raw_batch_file_path, file_name)
            df.to_csv(feature_store_file_path, index=False, header=True)

            return feature_store_file_path

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def initiate_data_ingestion(self):

        logging.info("Initiating data ingestion component of training pipeline")

        try:
            self.export_data_into_raw_data_dir()

            logging.info("Data ingestion completed")

            return self.data_ingestion_config.data_ingestion_dir

        except Exception as e:
            raise VisibilityException(e, sys) from e