import sys
from typing import Generator,List,Tuple
import os
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from src.constant import *
from src.exception import VisibilityException
from src.logger import logging
from src.utils.main_utils import MainUtils
from src.cloud_storage.aws_syncer import S3Sync

from dataclasses import dataclass

@dataclass

class ModeTrainerConfig:
    model_trainer_dir:str = os.path.join(artifact_folder,"model_trainer")
    trained_model_path = os.path.join(model_trainer_dir,"trained_model","model.pkl")
    expected_accuracy = 0.6
    model_config_file_path = os.path.join('config','model.yaml')


class VisibilityModel:
    
    def __init__(self,preprocessing_object:object,trainer_model_object:object):
        self.preprocessing_object = preprocessing_object
        self.trainer_model_object = trainer_model_object

    def predict(self,X:pd.DataFrame)->pd.DataFrame:
        logging.info("Entered the predict method of srcTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")
            transformed_features = self.preprocessing_object.transform(X)
            logging.info("used the trained model to get predictions")
            return self.trained_model_object.predict(transformed_features)
        except Exception as e:
            raise VisibilityException(e,sys)
        
    def __repr__(self):
        return f"{type(self.trainer_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.trainer_model_object).__name__}()"
    

class ModelTrainer:

    def __init__(self):
        self.model_trainer_config = ModeTrainerConfig()
        self.utils = MainUtils()

    
    def evaluate_models(self,X,y,models):
        try:
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
            model_report = {}

            for i in range(len(list(models))):
                model = list(models.values())[i]
                model.fit(X_train,y_train)
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)
                train_model_score = r2_score(y_train,y_train_pred)
                test_model_score = r2_score(y_test,y_test_pred)
                model_report[list(models.keys())[i]] = test_model_score

        except Exception as e:
            raise VisibilityException(e,sys)
        
    def get_best_model(self,X_train:np.array,y_train:np.array,X_test:np.array,y_test:np.array,models:dict):
        try:
            model_report = self.evaluate_models(X_train,y_train,X_test,y_test,models)
            print(model_report)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model_object = models[best_model_name]
            logging.info(f"Best model found on both training and testing dataset is {best_model_name} with r2 score of {best_model_score}")
            return best_model_name,best_model_object,best_model_score
        except Exception as e:
            raise VisibilityException(e,sys)
    
    
    def fine_tune_model(self,best_model_object:object,best_model_name:str,X_train,y_train,)->object:
        try:
            model_param_grid = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)["model_selection"]["model"][best_model_name]["search_param_grid"]
            grid_search = GridSearchCV(best_model_object,param_grid = model_param_grid,cv = 5,n_jobs = -1,verbose = 1)
            grid_search.fit(X_train,y_train)
            best_params = grid_search.best_params_
            print("best_params are: ",best_params)
            fine_tuned_model = best_model_object.set_params(**best_params)

            return fine_tuned_model
        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    
    def initiate_model_trainer(self,train_array,test_array,preprocessor_path):
        try:
            logging.info("Splitting training and testing input data")
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(),
                'Lasso Regression': Lasso(),
                'Random Forest Regressor': RandomForestRegressor(),
                'Gradient Boosting Regressor': GradientBoostingRegressor()
            }

            logging.info(f"Extracting preprocessor object from path: {preprocessor_path}")

            preprocessor = self.utils.load_object(file_path = preprocessor_path)

            logging.info("Extracting model config file path")

            model_report:dict = self.evaluate_models(X_train,y_train,model = models)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_models = models[best_model_name]

            best_models = self.fine_tune_model(
                best_model_name = best_model_name,
                best_model_object= best_models,
                X_train = X_train,
                y_train = y_train
            )

            best_models.fit(X_train,y_train)
            y_pred = best_models.predict(X_test)
            best_models_score = r2_score(y_test,y_pred)
            print(best_models_score)

            if best_models_score < self.model_trainer_config.expected_accuracy:
                raise VisibilityException("No best model found with score greater than expected accuracy")
            
            logging.info(f"Best model found is {best_model_name} with r2 score of {best_models_score}")

            custom_model = VisibilityModel(preprocessing_object=preprocessor,trainer_model_object=best_models)

            logging.info(f"Saving the best model at path: {self.model_trainer_config.trained_model_path}")

            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path),exist_ok=True)

            self.utils.save_object(file_path = self.model_trainer_config.trained_model_path,obj = custom_model)

            self.s3_sync.sync_folder_to_S3(folder = os.path.dirname(self.model_trainer_config.trained_model_path),
                                           aws_bucket_name = AWS_S3_BUCKET_NAME)

            return best_models_score
        
        except Exception as e:
            raise VisibilityException(e,sys)
        


            