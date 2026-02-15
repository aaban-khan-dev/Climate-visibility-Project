import sys
from typing import Dict,Tuple
import os
import pandas as pd
import pickle
import yaml

from src.exception import VisibilityException
from src.logger import logging
from src.constant import *

class MainUtils:
    
    def __init__(self):
        pass

    def read_yaml_file(self,filename:str)->Dict:
        try:
            with open(filename,"rb") as yaml_file:
                return yaml.safe_load(yaml_file)
            
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    def read_schema_config_file(self)->Dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config","schema.yaml"))
            return schema_config
        except Exception as e:
            raise VisibilityException(e,sys) from e
        

    @staticmethod
    def save_object(file_path:str,obj:object)->None:
        logging.info(f"Entered the save_object method of MainUtils class")
        try:
            with open(file_path,"wb") as file_obj:
                pickle.dump(obj,file_obj)
            logging.info(f"Exited the save_object method of MainUtils class")
        except Exception as e:
            raise VisibilityException(e,sys) from e
        
    @staticmethod
    def load_object(file_path:str)->object:
        logging.info(f"Entered the load_object method of MainUtils class")
        try:
            with open(file_path,"rb") as file_obj:
                return pickle.load(file_obj)
            logging.info(f"Exited the load_object method of MainUtils class")
        except Exception as e:
            raise VisibilityException(e,sys) from e