import json
import os
import boto3

sns = boto3.client('sns')
TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    for record in event['Records']:
        item = json.loads(record['body'])
        tiket = item['tiket']
        nama = item['nama']
        masalah = item['masalah']
        message = f'Tiket: {tiket}\nNama: {nama}\nMasalah: {masalah}\nStatus: Diproses (simulasi)'
        sns.publish(TopicArn=TOPIC_ARN, Subject='Laporan Layanan IT Masuk', Message=message)
        print(json.dumps({'event':'processed','tiket':tiket},ensure_ascii=False))
    return {'status':'ok'}
