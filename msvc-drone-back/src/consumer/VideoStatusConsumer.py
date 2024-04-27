import json
import os

import pika
from src.database.declarative_base import open_session
from src.models.Video import Video

# Establishing queue connection
amqp_conn_url = os.environ.get('RABBITMQ_URL_CONNECTION')
print(f'Connection string: {amqp_conn_url}')

url_parameters = pika.URLParameters(amqp_conn_url)
connection = pika.BlockingConnection(url_parameters)

consume_channel = connection.channel()
consume_channel.queue_declare(queue='video-drone-queue-status')


def receive_worker_processing_response(ch, method, properties, body: bytes):
    print('Update the processed video')
    json_received = json.loads(body.decode('utf-8'))

    session = open_session()

    video_processed = session.query(Video).filter(Video.video_id == json_received['filename']).one_or_none()
    if video_processed:
        video_processed.status = json_received['video_status']
        video_processed.path = json_received['new_video_path']
        session.commit()
        session.close()

    print(f'Video processed: {json_received["filename"]}')


consume_channel.basic_consume(queue='video-drone-queue-status',
                              on_message_callback=receive_worker_processing_response,
                              auto_ack=True)
