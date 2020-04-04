import json
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from datetime import datetime

#IAM
ACCESS_KEY=os.environ.get('ACCESS_KEY')
SECRET_KEY=os.environ.get('SECRET_KEY')
# S3 연결
s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
# Rekognition 연결
rekognition = boto3.client('rekognition',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
# DynamoDB 연결
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)

# DynamoDB Insert
# 1번째 매개변수 : 이미지 특정번호
# 2번째 매개변수 : 텍스트로 변환된 값
def set_dynamodb(img_no,text,max_text):
    print('img_no ======> ',img_no)
    print('text ========> ',text)
    print('max_text ====> ',max_text)
    
    table = dynamodb.Table('imgConvertText')
    table.put_item(
        Item={
            'imgNo' : img_no,
            'text' : text,
            'maxText': max_text,
            'imgDate' : datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        }
    )

# rekognition 이미지 텍스트 변환
# 1번째 매개변수 : S3 버킷이름
# 2번째 매개변수 : S3에 저장한 객체(이미지,파일,영상 등등)
def convert_text(bucket_name,key):
    print('bucket_name ====> ', bucket_name)
    print('key ============> ', key)
    response = rekognition.detect_text(
    Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name' : key
            }    
        }    
    )
    json_res = json.dumps(response)
    dict = json.loads(json_res)
    text_list = []
    for i in dict['TextDetections']:
        text_list.append(i['DetectedText'])
        
    return text_list

# rekognition에서 반환된 결과중에 가장 근접한 Text 찾기
def get_max_text(str):
    max_len_text = ''
    max_num = 0
    for i in str:
        index_len = len(i)
        if max_num < index_len:
            max_len_text = i
            max_num = index_len
    return max_len_text
    
def lambda_handler(event, context):

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
    
    str = convert_text(bucket,key)
    print('Convert image to text ======> ',str)
    max_str = get_max_text(str)
    print('max len text ===============> ',max_str)
    # key값에 이미지 업로드 된 전체경로가 오기 때문에 split으로 사진이름을 추출한다.
    img_no = key.split('/')
    set_dynamodb(img_no[len(img_no)-1],str,max_str)
    
    return {
        'statusCode': 200,
        'body': json.dumps('hello')
    }