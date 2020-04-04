import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

#IAM
ACCESS_KEY=os.environ.get('ACCESS_KEY')
SECRET_KEY=os.environ.get('SECRET_KEY')
# DynamoDB 연결
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
    
def lambda_handler(event, context):
    
    # API 인자로 사진 이름을 받는다.
    imgNo = event['imgNo']
    table = dynamodb.Table('imgConvertText')
    # Full scan
    response = table.query(
        KeyConditionExpression=Key('imgNo').eq(imgNo)
    )
    items = response['Items']
    return {
        'statusCode': 200,
        'body': items
    }