import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')

def translate(event, context):

    # obtenemos el idioma de destino de la solicitud
    target_lang=event['pathParameters']['language']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # recuperamos todo desde la base de datos
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
        
    # obtenemos el get del servicio translate
    translate = boto3.client(service_name='translate', region_name='us-east-1')
    
    translated_text = translate.translate_text(Text=result['Item']['text'], 
                SourceLanguageCode="auto", TargetLanguageCode=target_lang)
    
    # traducimos el texto
    result['Item']['text']=translated_text.get('TranslatedText')

    # response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response