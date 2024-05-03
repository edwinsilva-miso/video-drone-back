import json
import os

import pika
from google.cloud import storage

from src.services.VideoProcessingService import VideoProcessingService

# Establishing queue connection
url_parameters = pika.URLParameters(os.environ.get('RABBITMQ_URL_CONNECTION'))
connection = pika.BlockingConnection(url_parameters)

publish_channel = connection.channel()
publish_channel.queue_declare(queue='video-drone-queue-status')

consume_channel = connection.channel()
consume_channel.queue_declare(queue='video-drone-queue')

delete_channel = connection.channel()
delete_channel.queue_declare(queue='video-drone-delete-queue')


BUCKET_NAME: str = os.environ.get('DRONE_BUCKET', 'msvc-drone-bucket')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS', 'videos')
SECRET_PATH: str = os.environ.get('SECRET_PATH')


def process_video_task(ch, method, properties, body):
    json_received = json.loads(body.decode('utf-8'))

    local_file_path = f'/tmp/{json_received["filename"]}'
    cloud_file_path = f'{PATH_TO_VIDEOS}/{json_received["filename"]}'

    storage_client = storage.Client.from_service_account_json(SECRET_PATH)
    bucket = storage_client.bucket(BUCKET_NAME)
    cloud_blob = bucket.blob(cloud_file_path)
    cloud_blob.download_to_filename(local_file_path)

    data = VideoProcessingService.process_video(file_path=local_file_path)

    blob = bucket.blob(f'{PATH_TO_VIDEOS}/{data["edited_video_name"]}')
    blob.upload_from_filename(data['new_file_path'], content_type='video/mp4')

    # clear storage in the device containing the worker
    os.remove(local_file_path)
    os.remove(data["new_file_path"])

    # Send queue message
    publish_channel.basic_publish(exchange='', routing_key='video-drone-queue-status', body=json.dumps(data))

    print(f'Video processed {json_received["filename"]}')


consume_channel.basic_consume(queue='video-drone-queue',
                              on_message_callback=process_video_task,
                              auto_ack=True)
