import json
import os
import uuid
import boto3

sqs = boto3.client('sqs')
QUEUE_URL = os.environ['SQS_QUEUE_URL']

def response(status, data):
    return {'statusCode': status, 'headers': {'content-type':'application/json'}, 'body': json.dumps(data, ensure_ascii=False)}

def lambda_handler(event, context):
    try:
        raw = event.get('body') or '{}'
        if event.get('isBase64Encoded'):
            import base64
            raw = base64.b64decode(raw).decode('utf-8')
        data = json.loads(raw)
        if not isinstance(data, dict):
            return response(400, {'error':'Data harus objek JSON'})
        nama = str(data.get('nama','')).strip()
        masalah = str(data.get('masalah','')).strip()
        if not (2 <= len(nama) <= 80 and 5 <= len(masalah) <= 500):
            return response(400, {'error':'Nama 2-80 karakter dan masalah 5-500 karakter wajib diisi'})
        tiket = str(uuid.uuid4())
        payload = {'tiket': tiket, 'nama': nama, 'masalah': masalah}
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(payload, ensure_ascii=False))
        print(json.dumps({'event':'queued','tiket':tiket},ensure_ascii=False))
        return response(202, {'status':'diterima','tiket':tiket,'pesan':'Permintaan masuk antrean'})
    except (ValueError, UnicodeDecodeError, TypeError):
        return response(400, {'error':'Format JSON tidak valid'})
    except Exception:
        print('ERROR: gagal mengirim pesan ke SQS', flush=True)
        raise
