from pandas import DataFrame
from sklearn.pipeline import Pipeline
from src.exception import VisibilityException
from src.logger import logging

import sys,os
from dataclasses import dataclass


class VisibilityModel:

    def __init__(self,preprocessing_object:Pipeline,trainer_model_object:object):
        self.preprocessing_object = preprocessing_object
        self.trainer_model_object = trainer_model_object

    def predict(self,dataframe:DataFrame)->DataFrame:
        logging.info("Entered the predict method of srcTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")
            transformed_features = self.preprocessing_object.transform(dataframe)
            logging.info("used the trained model to get predictions")
            return self.trainer_model_object.predict(transformed_features)
        except Exception as e:
            raise VisibilityException(e,sys)
        
    def __repr__(self):
        return f"{type(self.trainer_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trainer_model_object).__name__}()"
     