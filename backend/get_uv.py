import boto3
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('city-uv-index')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  

    try:
        query_params = event.get('queryStringParameters', {})
        print("Query parameters:", query_params)  

        city = query_params.get('city')
        city = 'Uv ' + city
        if not city:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing city parameter'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            }

        response = table.query(
            KeyConditionExpression='city = :city',
            ExpressionAttributeValues={
                ':city': city,
            },
        )

        items = response.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps(items, cls=DecimalEncoder),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        }