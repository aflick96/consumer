import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv

def fetch_recent_files(bucket_name):
    load_dotenv('dev.env')
    
    print(os.getenv('AWS_ACCESS_KEY_ID'))
    print(os.getenv('AWS_SECRET_ACCESS_KEY'))

    try:
        # Initialize the S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            verify=False
        )

        # List objects in the bucket, ordered by the last modified date
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print(f"No objects found in bucket {bucket_name}.")
            return

        # Sort the files by the LastModified field (descending)
        sorted_files = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)

        # Print out the two most recent files
        print("The two most recent files in the S3 bucket are:")
        for obj in sorted_files[:2]:  # Get the top 2 most recent files
            print(f"File: {obj['Key']}, Last Modified: {obj['LastModified']}")

    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    bucket_name = 'dvc-bucket1'
    fetch_recent_files(bucket_name)
