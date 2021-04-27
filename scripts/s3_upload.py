import os
import boto3
from decouple import config
from datetime import datetime, timedelta

s3_client = boto3.client('s3')
bucket = config('S3_BUCKET_NAME')
folder = 'noise_audio'


def upload_files_to_s3(local_dir_path):
    date_today = get_today_date()
    for filename in os.listdir(local_dir_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(local_dir_path, filename)
            s3_key = f'{folder}/{date_today}/{filename}'
            with open(file_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket, s3_key, ExtraArgs={'ContentType': 'application/json'})

def get_today_date():
    return (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d")


if __name__ == '__main__':
    upload_files_to_s3('.')