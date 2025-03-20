import boto3
import json
import base64
from decimal import Decimal
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

AES_KEY = b'sun-protection12'
AES_IV = b'sun-protection34'

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def decrypt_data(encrypted_data):
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return json.loads(decrypted_bytes.decode("utf-8"))
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def encrypt_data(data):
    try:
        data_json = json.dumps(data, cls=DecimalEncoder)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        padded_data = pad(data_json.encode('utf-8'), AES.block_size)
        encrypted_bytes = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        print(f"Encryption failed: {e}")
        return None

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('city-uv-index')

def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # 允许所有源访问
        'Access-Control-Allow-Methods': 'GET,OPTIONS',  # 允许的 HTTP 方法
        'Access-Control-Allow-Headers': 'Content-Type'  # 允许的头部
    }

    print("Event:", json.dumps(event))
    query_params = event.get('queryStringParameters', {})
    encrypted_city = query_params.get('city')

    if not encrypted_city:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing city parameter'}),
            'headers': headers,
        }

    decrypted_params = decrypt_data(encrypted_city)
    if not decrypted_params or 'city' not in decrypted_params:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid city parameter'}),
            'headers': headers,
        }

    city = 'Uv ' + decrypted_params['city']
    print("Querying for city:", city)

    try:
        response = table.query(
            KeyConditionExpression='city = :city',
            ExpressionAttributeValues={':city': city}
        )
        items = response.get('Items', [])
        encrypted_response = encrypt_data(items)
        return {
            'statusCode': 200,
            'body': encrypted_response,
            'headers': headers,
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': headers,
        }