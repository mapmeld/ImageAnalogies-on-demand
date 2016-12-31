# s3upload
# use the boto library to upload new photos to S3
# based on http://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto

import boto
import boto.s3
import sys
from boto.s3.key import Key
from os import environ

AWS_ACCESS_KEY_ID = environ['ACCESSKEY']
AWS_SECRET_ACCESS_KEY = environ['SECRETKEY']

bucket = None

def create_bucket(task_id):
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket_name = task_id
    bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

def upload_results(task_id, files_to_upload):
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket_name = task_id
    
    for file in files_to_upload:
        k = Key(bucket)
        k.key = file
        k.set_contents_from_filename('./output/' + file)