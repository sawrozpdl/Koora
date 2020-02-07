import boto3
import os
from botocore.client import Config

ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY']
ACCESS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
BUCKET_NAME = os.environ['AWS_BUCKET_NAME']

#BUCKET_LOCATION = boto3.client('s3').get_bucket_location(Bucket=BUCKET_NAME)

# SETUP S3 CREDENTIALS

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

s3_bucket = s3.Bucket(BUCKET_NAME)

# Directly upload the given file


def upload(file, fileName):

    s3_bucket.put_object(
        Key=fileName, Body=file, ACL='public-read')

    file_url = "https://s3.amazonaws.com/{0}/{1}".format(BUCKET_NAME, fileName)
    return file_url


# Upload file located at directory
# rb -> binary read (for images)
# rt -> text read (for other files)

def findAndUpload(directory, fileName, binaryMode):
    readMode = 'rb' if binaryMode else 'rt'
    file = open(directory, readMode)
    s3.Bucket(BUCKET_NAME).put_object(
        Key=fileName, Body=file, ACL='public-read')


def delete(key):
    s3.Object(BUCKET_NAME, key).delete()