from decouple import config

from src.services.VideoProcessingService import VideoProcessingService

import pika

# Establishing queue connection
rabbit_url = config('RABBITMQ_URL_CONNECTION')
url_parameters = pika.URLParameters(rabbit_url)
connection = pika.BlockingConnection(url_parameters)
channel = connection.channel()
channel.queue_declare(queue='video-drone-queue')


def save_video_task():

    method_frame, header_frame, body = channel.basic_get(queue='video-drone-queue', auto_ack=True)
    if method_frame:
        message = body.decode('utf-8')
        result = VideoProcessingService.save_video(message)

        # Send queue message
        channel.basic_publish(exchange='', routing_key='video-drone-queue-status', body=result)
        print('Video processed')

