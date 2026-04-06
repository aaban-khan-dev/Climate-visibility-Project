import sys,os

from src.component.data_ingestion import DataIngestion
from src.component.data_transformation import DataTransformation
from src.component.data_validation import DataValidation
from src.component.model_trainer import ModelTrainer
from dataclasses import dataclass
from datetime import datetime
from src.exception import VisibilityException
from src.logger import logging

class TrainingPipeline:


    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            raw_data_dir = data_ingestion.initiate_data_ingestion()
            return raw_data_dir
        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    
    def start_data_validation(self,raw_data_dir):
        try:
            data_validation = DataValidation(raw_data_store_dir = raw_data_dir)
            validation_data_dir = data_validation.initiate_data_validation()
            return validation_data_dir
        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    def start_data_transformation(self,validation_data_dir):
        try:
            data_transformation = DataTransformation(valid_data_dir = validation_data_dir)
            train_arr,test_arr,preprocessor_path = data_transformation.initiate_data_transformation()
            return train_arr,test_arr,preprocessor_path        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    def start_model_trainer(self,train_arr,test_arr,preprocessor_path):
        try:
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(train_arr,test_arr,preprocessor_path)
            return model_score
        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    
    def run_pipeline(self):
        try:
            raw_data_dir = self.start_data_ingestion()
            validation_data_dir = self.start_data_validation(raw_data_dir)
            train_arr,test_arr,preprocessor_path = self.start_data_transformation(validation_data_dir)
            r2_squared = self.start_model_trainer(train_arr,test_arr,preprocessor_path)

            print("training completed: training model score: {r2_squared}")
            
            logging.info("training completed: training model score: ",r2_squared)

        except Exception as e:
            raise VisibilityException(e,sys)
                