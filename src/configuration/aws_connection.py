import boto3
import os
from dotenv import load_dotenv
from src.constant import REGION_NAME

class S3Client:

    s3_client = None
    s3_resource = None

    def __init__(self,region_name = REGION_NAME):

        if S3Client.s3_clinet == None or S3Client.s3_resource == None:
            __access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            __secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            if __access_key_id == None or __secret_access_key == None:
                raise Exception("AWS credentials are not set in environment variables")
            
            S3Client.s3_resource = boto3.resource('s3',aws_access_key_id = __access_key_id,
                                                  aws_secret_access_key = __secret_access_key,region_name = region_name)
            
            S3Client.s3_client = boto3.client('s3',aws_access_key_id = __access_key_id,
                                                  aws_secret_access_key = __secret_access_key,region_name = region_name)
            

        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource


    



