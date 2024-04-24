from decouple import config

from src.services.VideoUploadService import VideoUploadService

import pika

# Establishing queue connection
rabbit_url = config('RABBITMQ_URL_CONNECTION')
url_parameters = pika.URLParameters(rabbit_url)
connection = pika.BlockingConnection(url_parameters)
channel = connection.channel()
channel.queue_declare(queue='video-drone-queue-status')


def get_video_status():
    method_frame, header_frame, body = channel.basic_get(queue='video-drone-queue-status', auto_ack=True)
    if method_frame:
        message = body.decode('utf-8')
        if message:
            content = message.split(": ", 3)
            filename = content[0]
            status = content[1]
            new_video_path = content[2]

            VideoUploadService.update_video_process(filename, status, new_video_path)
