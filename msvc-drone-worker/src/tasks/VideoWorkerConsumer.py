# Establishing queue connection
import json
import logging
import os
import threading

from google.api_core import retry
from google.cloud import storage, pubsub_v1
from sqlalchemy import func

from src.database.database import ProcessingTask, open_session
from src.services.VideoProcessingService import VideoProcessingService

BUCKET_NAME: str = os.environ.get('DRONE_BUCKET', 'msvc-drone-bucket')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS', 'videos')
SECRET_PATH: str = os.environ.get('SECRET_PATH')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SECRET_PATH
PROJECT_ID: str = os.environ.get('PROJECT_ID')
VIDEO_UPLOAD_SUBSCRIPTION: str = os.environ.get('VIDEO_UPLOAD_SUBSCRIPTION')
VIDEO_PROCESSING_TOPIC: str = os.environ.get('VIDEO_PROCESSING_TOPIC')

logging.basicConfig(level=logging.INFO)


def process_video_task(filename: str):
    local_file_path = f'/tmp/{filename}'
    cloud_file_path = f'{PATH_TO_VIDEOS}/{filename}'

    storage_client = storage.Client.from_service_account_json(SECRET_PATH)
    bucket = storage_client.bucket(BUCKET_NAME)
    cloud_blob = bucket.blob(cloud_file_path)
    cloud_blob.download_to_filename(local_file_path)

    data: dict = VideoProcessingService.process_video(file_path=local_file_path)

    blob = bucket.blob(f'{PATH_TO_VIDEOS}/{data['edited_video_name']}')
    blob.upload_from_filename(data['new_file_path'], content_type='video/mp4')
    logging.log(level=logging.INFO, msg=f'Video processed {filename}')

    # clear storage in the device containing the worker
    os.remove(local_file_path)
    os.remove(data['new_file_path'])
    logging.log(level=logging.INFO, msg=f'Freed local storage {local_file_path}, {data["new_file_path"]}')

    # Send message
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, VIDEO_PROCESSING_TOPIC)

    future = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))

    logging.log(level=logging.INFO, msg=f'Published message id {future.result()}')


def pull_next_message():
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PROJECT_ID, VIDEO_UPLOAD_SUBSCRIPTION)

        with subscriber:
            response = subscriber.pull(
                request={'subscription': subscription_path, 'max_messages': 1},
                retry=retry.Retry(deadline=300),
            )

            if len(response.received_messages) > 0:
                message = response.received_messages[0]

                body = message.message.data
                logging.log(level=logging.INFO, msg=f'Received: {body}.')
                session = open_session()
                json_received = json.loads(body.decode('utf-8'))

                session.add(ProcessingTask(video_id=json_received['filename']))
                session.commit()
                session.close()

                process_video_task(json_received['filename'])

                # Acknowledges the received messages, so they will not be sent again.
                subscriber.acknowledge(request={'subscription': subscription_path, 'ack_ids': [message.ack_id]})
                logging.log(level=logging.INFO,
                            msg=f'Received and acknowledged {len(response.received_messages)} message.')
            else:
                logging.log(level=logging.INFO, msg=f'No messages received for worker consumer.')
    except Exception as e:
        logging.log(level=logging.ERROR, msg=f'Exception: {e}')
