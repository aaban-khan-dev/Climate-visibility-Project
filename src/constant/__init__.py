from datetime import datetime
import os


AWS_S3_BUCKET_NAME = "climate-visibility.123"
MONGO_DATABASE_NAME = "Visibility"
MONGO_COLLECTION_NAME = "data"

TARGET_COLUMN = "VISIBILITY"
CLUSTER_LABEL_COLUMN = "Cluster"

MODEL_FILE_NAME = "model"
MODEL_FILE_EXTENSION = ".pkl"

artifact_folder_name = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
artifact_folder =  os.path.join("artifacts", artifact_folder_name)

REGION_NAME = os.getenv("REGION_NAME")