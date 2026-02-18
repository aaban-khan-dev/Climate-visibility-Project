from datetime import date
import sys
import os
from typing import List
import pandas as pd
import re
import shutil

from src.constant import *
from src.exception import VisibilityException
from src.logger import logging
from src.utils import MainUtils
from dataclasses import dataclass

sample_file_name = "visibility_08012020_120000.csv"
LENGTH_OF_DATE_STAMP = 8
LENGTH_OF_TIME_STAMP = 6
NUMBER_OF_COLUMNS = 5

@dataclass
class DataValidationConfig:
    data_validation_dir:str = os.path.join(artifact_folder,"data_validation")
    valid_data_dir:str = os.path.join(data_validation_dir,"valid_data")
    invalid_data_dir:str = os.path.join(data_validation_dir,"invalid_data")

class Datavalidation:
    def __init__(self,raw_data_store_dir:str):
        self.raw_data_store_dir = raw_data_store_dir
        self.data_validation_config = DataValidationConfig()
        self.main_utils = MainUtils()
        self._schema_config = self.main_utils.read_schema_config_file()
    
    def validate_file_name(self,file_path:str)->bool:
        """
        Method Name: validate_file_name
        Description: This method validates the file name of a particular raw file
        Output : True or False value is returned based on the schema
        On Failure : write exception log and raise exception
        """
        try:
            file_name = os.path.basename(file_path)
            regex = "visibility_[\d_]+[\d]+\.csv"
            if (re.match(regex,file_name)):
                split_at_dot = re.split(".csv",file_name)
                split_at_underscore = re.split("_",split_at_dot[0])
                date_stamp = split_at_underscore[1]
                time_stamp = split_at_underscore[2]

                if len(date_stamp) == LENGTH_OF_DATE_STAMP and len(time_stamp) == LENGTH_OF_TIME_STAMP:
                    return True 
                else:
                    return False
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    def validate_number_of_columns(self,file_path:str)->bool:
        """
        Method Name: validate_number_of_columns
        Description: This method validates the number of columns in a particular raw file
        Output : True or False value is returned based on the schema
        On Failure : write exception log and raise exception
        """
        try:
            df = pd.read_csv(file_path)
            column_lenght_validation_status = len(df.columns) == len(self._schema_config["columns"])
            return column_lenght_validation_status
        except Exception as e:
            raise VisibilityException(e,sys) from e 
        
    def validate_missing_values_in_whole_column(self,file_path:str)->bool:
        """
        Method Name: validate_missing_values_in_whole_column
        Description: This method validates if there are any column in the raw file which has all values missing
        Output : True or False value is returned based on the schema
        On Failure : write exception log and raise exception
        """
        try:
            df = pd.read_csv(file_path)
            no_of_columns_with_whole_missing_values = 0
            for column in df:
                if(len(df[column]) - df[column].count()) == len(df[column]):
                    no_of_columns_with_whole_missing_values += 1
                if no_of_columns_with_whole_missing_values > 0:
                    return False
                else:
                    return True
                
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    def get_raw_batch_file_path(self)-> List:
        """
        Method Name: get_raw_batch_file_path
        Description: This method returns the list of file paths for the raw files stored in the raw data directory
        Output : List of file paths is returned based on the schema
        On Failure : write exception log and raise exception
        """
        try:
            raw_batch_file_path = self.raw_data_store_dir
            file_list = os.listdir(raw_batch_file_path)
            file_path_list = [os.path.join(raw_batch_file_path,file) for file in file_list]
            return file_path_list
        
        except Exception as e:
            raise VisibilityException(e,sys) from e
    
    def move_raw_files_to_validation_dir(self,src_path:str,dst_path:str):
        """
        Method Name: move_raw_files_to_validation_dir
        Description : This method moves the validated raw files to the validated directory
        Output : None
        On Failure : write exception log and raise exception
        """
        try:
           os.makedirs(dst_path,exist_ok = True)
           if os.basename(src_path) not in os.listdir(dst_path):
               shutil.move(src_path,dst_path)
        
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    def validate_raw_files(self)->bool:
        """
        Method Name: validate_raw_files
        Description : This method validates the raw files for training 
        Output : True or False value is returned based on validated file number
        On Failure : write exception log and raise exception
        """
        try:
            raw_batch_file_path = self.get_raw_batch_file_path()
            validated_file_count = 0
            for raw_file in raw_batch_file_path:
                file_name_validation_statuse = self.validate_file_name(raw_file)
                column_lenght_validation_status = self.validate_number_of_columns(raw_file)
                missing_values_in_whole_column_status = self.validate_missing_values_in_whole_column(raw_file)
                if(file_name_validation_statuse
                   and column_lenght_validation_status
                   and missing_values_in_whole_column_status):
                    validated_file_count += 1
                    self.move_raw_files_to_validation_dir(raw_file,self.data_validation_config.valid_data_dir)
                else:
                    self.move_raw_files_to_validation_dir(raw_file,self.data_validation_config.invalid_data_dir)
                
            valid_status = validated_file_count>0
            return valid_status
        
        except Exception as e:
            raise VisibilityException(e,sys) from e
    
    def initiate_data_validation(self):
        """
        Method Name: initiate_data_validation
        Description : This method initiates the data validation for training pipeline
        Output : None
        On Failure : write exception log and raise exception
        """
        try:
            logging.info("Entered the initiate_data_validation method of DataValidation class")
            validation_status = self.validate_raw_files()
            if validation_status:
                valid_data_dir = self.data_validation_config.valid_data_dir
                logging.info(f"Data Validation is completed and valid files are stored in valid directory : {valid_data_dir}")
            else:
                raise Exception("No data could be validated . Pipeline stopped")
            logging.info("Exited the initiate_data_validation method of DataValidation class")
        
        except Exception as e:
            raise VisibilityException(e,sys) from e