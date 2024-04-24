import json

from decouple import config

from src.services.VideoProcessingService import VideoProcessingService

import pika

# Establishing queue connection
url_parameters = pika.URLParameters(config('RABBITMQ_URL_CONNECTION'))
connection = pika.BlockingConnection(url_parameters)

publish_channel = connection.channel()
publish_channel.queue_declare(queue='video-drone-queue-status')

consume_channel = connection.channel()
consume_channel.queue_declare(queue='video-drone-queue')


def process_video_task(ch, method, properties, body):
    json_received = json.loads(body.decode('utf-8'))

    # TODO process the video

    # Send queue message
    publish_channel.basic_publish(exchange='', routing_key='video-drone-queue-status', body=json.dumps({
        'video_status': 'processed',
        'filename': json_received['filename'],
        'new_video_path': 'TODO'
    }))

    print(f'Video processed {json_received["filename"]}')


consume_channel.basic_consume(queue='video-drone-queue',
                              on_message_callback=process_video_task,
                              auto_ack=True)
