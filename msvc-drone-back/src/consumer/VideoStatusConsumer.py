import json
import logging
import os

from google.api_core import retry
from google.cloud import pubsub_v1

from src.database.declarative_base import open_session
from src.models.Video import Video

PROJECT_ID: str = os.environ.get('PROJECT_ID')
VIDEO_PROCESSING_SUBSCRIPTION: str = os.environ.get('VIDEO_PROCESSING_SUBSCRIPTION')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('SECRET_PATH')

logging.basicConfig(level=logging.INFO)


def pull_next_message():
    logging.log(level=logging.INFO, msg='getting next message')

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, VIDEO_PROCESSING_SUBSCRIPTION)

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

            video_processed = session.query(Video).filter(
                Video.video_id == json_received['original_file_name']).one_or_none()
            if video_processed:
                video_processed.status = json_received['status']
                video_processed.path = json_received['new_file_name']
                session.commit()
                session.close()

            # Acknowledges the received messages, so they will not be sent again.
            subscriber.acknowledge(request={'subscription': subscription_path, 'ack_ids': [message.ack_id]})
            logging.log(level=logging.INFO, msg=f'Received and acknowledged {len(response.received_messages)} message.')
        else:
            logging.log(level=logging.INFO, msg=f'No messages received.')
