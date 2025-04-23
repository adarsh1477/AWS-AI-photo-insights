import json
import boto3
import requests
from requests_aws4auth import AWS4Auth
import datetime
import os

# Initialize AWS clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

# OpenSearch config
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    service,
    session_token=credentials.token
)

es_endpoint = 'https://search-photos-le3xwoommwzx4noyzn2wtgt6ku.us-east-1.es.amazonaws.com'
index = 'photos'
headers = {'Content-Type': 'application/json'}

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        key = key.replace('%3A', ':').replace('+', ' ')

        print(f"Processing image: {key} from bucket: {bucket}")

        try:
            metadata = s3.head_object(Bucket=bucket, Key=key)
            meta = metadata.get('Metadata', {})
            print("Metadata received:", meta)

            custom_labels = []
            if 'customlabels' in meta:  
                custom_labels_str = meta['customlabels']
                custom_labels = [label.strip().lower() for label in custom_labels_str.split(',')]
                print(f"Custom labels found: {custom_labels}")

            created_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        except Exception as e:
            print(f"Error getting metadata: {str(e)}")
            custom_labels = []
            created_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        rekognition_response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=20,
            MinConfidence=70
        )

        rekognition_labels = [label['Name'].lower() for label in rekognition_response['Labels']]
        print(f"Rekognition labels: {rekognition_labels}")

        all_labels = custom_labels + rekognition_labels
        unique_labels = list(dict.fromkeys(all_labels))  # de-duplicate

        document = {
            'objectKey': key,
            'bucket': bucket,
            'createdTimestamp': created_timestamp,
            'labels': unique_labels
        }

        print(f"ElasticSearch document: {json.dumps(document)}")

        document_id = key.replace('/', '_')
        url = f"{es_endpoint}/{index}/_doc/{document_id}"
        auth = ('Google', 'Google#1')

        response = requests.put(url, auth=auth, json=document, headers=headers)

        if 200 <= response.status_code < 300:
            print(f"Document indexed successfully: {response.text}")
            return {
                'statusCode': 200,
                'body': json.dumps('Photo indexed successfully!')
            }
        else:
            print(f"Failed to index document: {response.text}")
            return {
                'statusCode': response.status_code,
                'body': json.dumps(f'Failed to index photo: {response.text}')
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error indexing photo: {str(e)}')
        }
