import subprocess

class S3Sync:

    def sync_folder_to_S3(self, folder, aws_bucket_name):
        """
        Sync local folder to S3 bucket
        """
        try:
            print(f"Uploading {folder} to s3://{aws_bucket_name}")

            result = subprocess.run(
                ["aws", "s3", "sync", folder, f"s3://{aws_bucket_name}", "--region", "eu-north-1"],
                capture_output=True,
                text=True
            )

            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            if result.returncode != 0:
                raise Exception("S3 upload failed")

            print("✅ Upload successful")

        except Exception as e:
            print("❌ Error during S3 upload:", e)


    def sync_folder_from_S3(self, folder, aws_bucket_name):
        """
        Sync S3 bucket to local folder
        """
        try:
            print(f"Downloading s3://{aws_bucket_name} to {folder}")

            result = subprocess.run(
                ["aws", "s3", "sync", f"s3://{aws_bucket_name}", folder, "--region", "eu-north-1"],
                capture_output=True,
                text=True
            )

            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            if result.returncode != 0:
                raise Exception("S3 download failed")

            print("✅ Download successful")

        except Exception as e:
            print("❌ Error during S3 download:", e)