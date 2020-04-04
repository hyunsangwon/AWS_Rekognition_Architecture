import json
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

# IAM
ACCESS_KEY=os.environ.get('ACCESS_KEY')
SECRET_KEY=os.environ.get('SECRET_KEY')

# S3 download 
def downloadFromS3(strBucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3_client.download_file(strBucket, s3_path, local_path)

# S3 upload  
def uploadToS3(bucket, s3_path, local_path):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3_client.upload_file(local_path, bucket, s3_path)
    
def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_path = event['Records'][0]['s3']['object']['key']
    file_name = file_path.split('/')[-1]
    # /tmp 는 lambda 안에 있는 임시 경로를 의미함(람다는 리눅스 기반)
    downloadFromS3(bucket_name, file_path, '/tmp/' + file_name)
    im = Image.open('/tmp/' + file_name)
    
    width_rate = 360
    height_rate = 480
    
    im = im.rotate(-90, expand=True)
    crop_rate = float(im.size[0]) / float(width_rate)  
    crop_width = im.size[0] - 1
    crop_height = int(height_rate * crop_rate)
    cropImage = im.crop((0, 0, crop_width, crop_height))

    # crop 하고 싶은 범위 설정
    partial_to_top_rate = 179
    partial_width_rate = 292
    partial_height_rate = 140
    partial_rate = float(im.size[0]) / float(width_rate)
        
    left = int( (width_rate - partial_width_rate) / 2 * partial_rate )
    top = int( partial_to_top_rate * partial_rate )
    right = int( partial_width_rate * partial_rate )
    bottom = int( partial_height_rate * partial_rate ) + top
        
    cropImage = cropImage.crop((left, top, right, bottom))
    new_file_name = '/tmp/'+file_name.replace('.jpg', '_modify.jpg')
    cropImage.save(new_file_name)
    uploadToS3(bucket_name,file_path.replace('input','user'),new_file_name)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }