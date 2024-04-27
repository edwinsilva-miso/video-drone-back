import json
import os

import pika
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


# noinspection PyInterpreter
def process_video_task(ch, method, properties, body):
    json_received = json.loads(body.decode('utf-8'))
    file = json_received['file']
    filename = json_received['filename']

    response = VideoProcessingService.save_video(file, filename)

    # Send queue message
    publish_channel.basic_publish(exchange='', routing_key='video-drone-queue-status', body=json.dumps({
        'video_status': response['status'],
        'filename': response['filename'],
        'new_video_path': response['path']
    }))

    print(f'Video processed {json_received["filename"]}')


def delete_video_task(ch, method, properties, body):
    json_received = json.loads(body.decode('utf-8'))
    video_path = json_received['video_path']

    VideoProcessingService.delete_video(video_path)


consume_channel.basic_consume(queue='video-drone-queue',
                              on_message_callback=process_video_task,
                              auto_ack=True)

delete_channel.basic_consume(queue='video-drone-delete-queue',
                             on_message_callback=delete_video_task,
                             auto_ack=True)
