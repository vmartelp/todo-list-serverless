import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def translate(event, context):

    # get target language from request
    target_lang=event['pathParameters']['language']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
        
    # get translate service
    translate = boto3.client(service_name='translate', region_name='us-east-1')
    
    translated_text = translate.translate_text(Text=result['Item']['text'], 
                SourceLanguageCode="auto", TargetLanguageCode=target_lang)
    
    # translate text
    result['Item']['text']=translated_text.get('TranslatedText')

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response