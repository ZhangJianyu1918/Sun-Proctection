import boto3
import csv
import urllib.parse
import re
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

# 初始化 S3 和 DynamoDB 客户端
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def normalize_column_name(col):
    col = col.replace('\ufeff', '')
    return col.lower().replace(' ', '_').replace('-', '_')

def lambda_handler(event, context):
    try:
        # 获取 S3 事件中的存储桶和文件信息
        if not event.get('Records') or len(event['Records']) == 0:
            raise ValueError("No records found in event data")
        
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # 从文件名提取城市名
        file_name = key.split('/')[-1]
        city_match = re.match(r'^([a-zA-Z-]+)(?:[_-])', file_name)
        if city_match:
            city = city_match.group(1).replace('-', ' ').title()
        else:
            city = 'Unknown'
            print(f"Can't get city name from {file_name}, use the default city name: {city}")
        
        # 流式下载和读取 CSV 文件
        response = s3_client.get_object(Bucket=bucket, Key=key)
        lines = []
        for line in response['Body'].iter_lines():
            decoded_line = line.decode('utf-8')
            lines.append(decoded_line)
        
        # 解析 CSV
        csv_reader = csv.DictReader(lines)
        
        # 打印实际列名以供调试
        actual_columns = csv_reader.fieldnames
        
        # 标准化列名并验证
        expected_columns = {'date_time', 'lat', 'lon', 'uv_index'}
        actual_columns_normalized = {normalize_column_name(col) for col in actual_columns}
        missing_columns = expected_columns - actual_columns_normalized
        if missing_columns:
            raise ValueError(f"CSV 文件 {key} 缺少必要列，缺少的列：{missing_columns}，实际列名：{actual_columns}")
        
        # 按日期分组并计算平均 UV Index
        daily_data = defaultdict(lambda: {'uv_sum': 0, 'count': 0, 'lat': None, 'lon': None})
        valid_rows = 0
        skipped_rows = 0
        for row in csv_reader:
            # 提取日期
            date_time_key = next(col for col in actual_columns if normalize_column_name(col) == 'date_time')
            date_time_str = row[date_time_key]
            try:
                date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                valid_rows += 1
            except ValueError as e:
                skipped_rows += 1
                continue
            
            # 累加 UV Index 和计数
            uv_index_key = next(col for col in actual_columns if normalize_column_name(col) == 'uv_index')
            try:
                uv_index = float(row[uv_index_key])
                daily_data[date]['uv_sum'] += uv_index
                daily_data[date]['count'] += 1
            except ValueError as e:
                skipped_rows += 1
                continue
            
            # 存储经纬度
            if daily_data[date]['lat'] is None:
                lat_key = next(col for col in actual_columns if normalize_column_name(col) == 'lat')
                lon_key = next(col for col in actual_columns if normalize_column_name(col) == 'lon')
                try:
                    daily_data[date]['lat'] = float(row[lat_key])
                    daily_data[date]['lon'] = float(row[lon_key])
                except ValueError as e:
                    skipped_rows += 1
                    continue
        
        
        # 连接到 DynamoDB 表
        table = dynamodb.Table('city-uv-index')  # 使用新表名
        
        # 批量写入 DynamoDB
        if not daily_data:
            print("There are valid data.")
        else:
            with table.batch_writer() as batch:
                for date, data in daily_data.items():
                    if data['count'] > 0:
                        avg_uv_index = Decimal(str(data['uv_sum'] / data['count']))
                        item = {
                            'city': city,  # 更新为新表的分区键
                            'date': date,
                            'lat': Decimal(str(data['lat'])),
                            'lon': Decimal(str(data['lon'])),
                            'avg_uv_index': avg_uv_index,
                        }
                        batch.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': f'Successfully imported {key} for {city} to DynamoDB with daily averages'
        }
    
    except Exception as e:
        print(f"处理失败: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error processing {key}: {str(e)}'
        }