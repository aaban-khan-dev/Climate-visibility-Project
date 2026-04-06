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
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

sample_file_name = "visibility_08012020_120000.csv"
LENGTH_OF_DATE_STAMP = 8
LENGTH_OF_TIME_STAMP = 6

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(artifact_folder, "data_validation")
    valid_data_dir: str = os.path.join(data_validation_dir, "valid_data")
    invalid_data_dir: str = os.path.join(data_validation_dir, "invalid_data")


class DataValidation:
    def __init__(self, raw_data_store_dir: str):
        self.raw_data_store_dir = raw_data_store_dir
        self.data_validation_config = DataValidationConfig()
        self.main_utils = MainUtils()
        self._schema_config = self.main_utils.read_schema_config_file()

    # ------------------- FILE NAME VALIDATION ------------------- #
    def validate_file_name(self, file_path: str) -> bool:
        try:
            file_name = os.path.basename(file_path)

            # Strict pattern: visibility_08012020_120000.csv
            pattern = r"^visibility_\d{8}_\d{6}\.csv$"

            if re.match(pattern, file_name):
                return True
            else:
                print(f"❌ Invalid filename format: {file_name}")
                return False

        except Exception as e:
            raise VisibilityException(e, sys) from e

    # ------------------- COLUMN COUNT VALIDATION ------------------- #
    def validate_number_of_columns(self, file_path: str) -> bool:
        try:
            df = pd.read_csv(file_path)

            expected_columns = [list(col.keys())[0] for col in self._schema_config["columns"]]
            actual_columns = list(df.columns)

            print(f"\n📊 Checking columns for: {file_path}")
            print("Expected:", expected_columns)
            print("Actual:", actual_columns)

            if actual_columns == expected_columns:
                return True
            else:
                print("❌ Column name mismatch")
                return False

        except Exception as e:
            raise VisibilityException(e, sys) from e

    # ------------------- MISSING VALUES VALIDATION ------------------- #
    def validate_missing_values_in_whole_column(self, file_path: str) -> bool:
        try:
            df = pd.read_csv(file_path)

            for column in df.columns:
                if df[column].count() == 0:
                    print(f"❌ Column '{column}' has all missing values")
                    return False

            return True

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def get_raw_batch_file_path(self) -> List:
        try:
            raw_batch_file_path = self.raw_data_store_dir
            file_list = os.listdir(raw_batch_file_path)

            print("\n📂 Files found:", file_list)

            file_path_list = [
                os.path.join(raw_batch_file_path, file) for file in file_list
            ]
            return file_path_list

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def move_raw_files_to_validation_dir(self, src_path: str, dst_path: str):
        try:
            os.makedirs(dst_path, exist_ok=True)

            if os.path.basename(src_path) not in os.listdir(dst_path):
                shutil.move(src_path, dst_path)

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def validate_raw_files(self) -> bool:
        try:
            raw_batch_file_path = self.get_raw_batch_file_path()

            validated_file_count = 0

            for raw_file in raw_batch_file_path:
                print(f"\n🔍 Validating file: {raw_file}")

                file_name_status = self.validate_file_name(raw_file)
                column_status = self.validate_number_of_columns(raw_file)
                missing_value_status = self.validate_missing_values_in_whole_column(raw_file)

                print("Result →",
                      f"Filename: {file_name_status},",
                      f"Columns: {column_status},",
                      f"Missing: {missing_value_status}")

                if file_name_status and column_status and missing_value_status:
                    validated_file_count += 1
                    print("✅ File is VALID")
                    self.move_raw_files_to_validation_dir(
                        raw_file, self.data_validation_config.valid_data_dir
                    )
                else:
                    print("❌ File is INVALID")
                    self.move_raw_files_to_validation_dir(
                        raw_file, self.data_validation_config.invalid_data_dir
                    )

            print(f"\n✅ Total valid files: {validated_file_count}")

            return validated_file_count > 0

        except Exception as e:
            raise VisibilityException(e, sys) from e

    def initiate_data_validation(self):
        try:
            logging.info("Entered data validation")

            validation_status = self.validate_raw_files()

            if validation_status:
                valid_data_dir = self.data_validation_config.valid_data_dir
                logging.info(
                    f"Data Validation completed. Valid files at: {valid_data_dir}"
                )
            else:
                raise Exception("No data could be validated. Pipeline stopped")

            logging.info("Exited data validation")
            return valid_data_dir

        except Exception as e:
            raise VisibilityException(e, sys) from e