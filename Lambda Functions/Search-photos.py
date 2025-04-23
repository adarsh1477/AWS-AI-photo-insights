import json
import boto3
import os
import base64
import requests

# AWS region and Lex bot/client setup
region = 'us-east-1'
lex = boto3.client('lexv2-runtime')

# OpenSearch endpoint and credentials
ELASTICSEARCH_HOST = 'https://search-photos-le3xwoommwzx4noyzn2wtgt6ku.us-east-1.es.amazonaws.com'
ES_USERNAME = os.environ['ES_USERNAME']
ES_PASSWORD = os.environ['ES_PASSWORD']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # 1. Parse query string
    qparams = event.get('queryStringParameters')
    if not qparams or 'q' not in qparams or not qparams['q'].strip():
        # No query provided
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'results': [], 'message': 'Please enter a label to search.'})
        }

    query = qparams['q'].strip()
    print("User query:", query)

    # 2. Get keywords from Lex (NLU)
    keywords = get_keywords_from_lex(query)
    print("Lex keywords:", keywords)

    if not keywords:
        # No keywords found by Lex
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'results': []})
        }

    # 3. Search in OpenSearch
    search_results = search_photos(keywords)
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'results': search_results})
    }

def get_keywords_from_lex(query):
    try:
        lex_response = lex.recognize_text(
            botId='6KGMSVMV9P',      # update to your actual Lex BotId
            botAliasId='TSTALIASID', # update to your actual Lex AliasId
            localeId='en_US',
            sessionId='web-session',  # can be any string, static is fine for stateless
            text=query
        )
        print("Lex response:", json.dumps(lex_response))

        # Extract keywords (all slots interpreted as strings)
        keywords = []
        for interp in lex_response.get('interpretations', []):
            intent = interp.get('intent', {})
            for slot_name, slot_value in (intent.get('slots') or {}).items():
                if slot_value and 'value' in slot_value and 'interpretedValue' in slot_value['value']:
                    val = slot_value['value']['interpretedValue']
                    if val: keywords.append(val.lower())
        print("Extracted keywords:", keywords)
        return keywords
    except Exception as e:
        print("Error in Lex:", str(e))
        return []

def search_photos(keywords):
    # Prepare the OpenSearch bool query with 'should' (OR)
    query_body = {
        "size": 20,
        "query": {
            "bool": {
                "should": [
                    {"match": {"labels": keyword}}
                    for keyword in keywords
                ]
            }
        }
    }
    print("OpenSearch query:", json.dumps(query_body))

    url = f"{ELASTICSEARCH_HOST}/photos/_search"
    auth_header = base64.b64encode(f"{ES_USERNAME}:{ES_PASSWORD}".encode()).decode()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_header}'
    }

    try:
        response = requests.get(
            url,
            data=json.dumps(query_body),
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        resp_json = response.json()
        print("OpenSearch response:", json.dumps(resp_json))

        results = []
        for hit in resp_json.get('hits', {}).get('hits', []):
            photo = hit.get('_source', {})
            # Only add if 'objectKey' and 'bucket' exist
            if 'objectKey' in photo and 'bucket' in photo:
                results.append({
                    'url': f"https://{photo['bucket']}.s3.amazonaws.com/{photo['objectKey']}",
                    'labels': photo.get('labels', [])
                })
        return results
    except Exception as e:
        print("Error searching OpenSearch:", str(e))
        return []
