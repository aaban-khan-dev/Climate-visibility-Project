from src.exception import VisibilityException
from src.cloud_storage.aws_storage import SimpleStorageService
from src.model.estimator import VisibilityModel
import sys
from pandas import DataFrame

class VisibilityEstimator:

    """
    This class is used to save and retrieve the visibility model in S3 bucket and do prediction

    """

    def __init__(self,bucket_name,model_name):
        self.bucket_name = bucket_name
        self.model_name = model_name
        self.s3 = SimpleStorageService()
        self.loaded_model:VisibilityModel = None

    
    def is_model_present(self,model_name):
        try:
            return self.s3.s3_key_path_available(self.bucket_name,model_name)
        
        except Exception as e:
            raise VisibilityException(e,sys)
        
    def load_model(self)->VisibilityModel:
        """
        Loads the model from model path
        """
        return self.s3.load_model(self.model_name,self.bucket_name)
    

    def save_model(self,from_file,remove:bool = False)->None:
        """
        Save the model to Model Path
        param from_file: local file path of the model to be uploaded
        param remove: By default false that means that the model will be locally available in our system
        """
        try:
            self.s3.upload_file(from_file,to_filename = self.model_name,bucket_name = self.bucket_name,remove=remove)

        except Exception as e:
            raise VisibilityException(e,sys)
        
    def predict(self,dataframe:DataFrame):

        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            
            return self.loaded_model.predict(dataframe)
        
        except Exception as e:
            raise VisibilityException(e,sys)


