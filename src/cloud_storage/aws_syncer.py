import os

class S3Sync:

    def sync_folder_to_S3(self,folder,aws_bucket_name):
        """
        Method Name: sync_folder_to_S3
        Description: This method syncs local folder to S3 bucket
        Output: None
        """

        command = f"aws s3 sync {folder} s3://{aws_bucket_name}"
        os.system(command)

    def sync_folder_from_S3(self,folder,aws_bucket_name):
        """
        Method Name: sync_folder_from_S3
        Description: This method syncs S3 bucket to local folder
        Output: None
        """

        command = f"aws s3 sync s3://{aws_bucket_name} {folder}"
        os.system(command)