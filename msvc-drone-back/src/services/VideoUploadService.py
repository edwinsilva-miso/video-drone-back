import base64
import datetime
import json
import os

import pika
from decouple import config
from flask import jsonify
from google.api_core.retry import Retry
from google.cloud import storage, pubsub_v1

from src.database.declarative_base import open_session
from src.models.User import User
from src.models.Video import Video, StatusVideo

BUCKET_NAME: str = os.environ.get('DRONE_BUCKET', 'msvc-drone-bucket')
PATH_TO_VIDEOS: str = os.environ.get('DRONE_PATH_TO_VIDEOS', 'videos')
SECRET_PATH: str = os.environ.get('SECRET_PATH')
VIDEO_UPLOAD_TOPIC: str = os.environ.get('VIDEO_UPLOAD_TOPIC')
PROJECT_ID: str = os.environ.get('PROJECT_ID')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SECRET_PATH


class VideoUploadService:

    @classmethod
    def upload(cls, description, video_name, user_id):
        """
        Implement here the video upload process
        """
        # These lines are a test for query videos for an user
        session = open_session()

        user = session.query(User).filter_by(id=user_id).first()

        if description:
            new_video = Video(
                description=description,
                video_id=video_name,
                path='',
                user_id=user.id,
                status=StatusVideo.uploaded
            )
            session.add(new_video)
            session.commit()
            session.close()
            return 'Video uploaded!'

        session.close()
        return False

    @classmethod
    def save_video_to_gcs(cls, file, filename):
        # Establishing queue connection
        storage_client = storage.Client.from_service_account_json(SECRET_PATH)
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f'{PATH_TO_VIDEOS}/{filename}')
        blob.upload_from_string(file.read(), content_type='video/mp4', retry=Retry(total=15, backoff_factor=0.1))

        # Send queue message
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, VIDEO_UPLOAD_TOPIC)

        data: dict = {'filename': filename}
        future = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))

        print(f'published message id {future.result()}')

        return 'Video sent to process'

    @classmethod
    def get_all_tasks(cls, user_id, order, maxim=None):
        session = open_session()

        if order == '0':
            videos = session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.asc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value,
                            'date': video.timestamp} for video in videos]
            response = videos_dict

        elif order == '1':
            videos = session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.desc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value,
                            'date': video.timestamp} for video in videos]
            response = videos_dict
        else:
            response = jsonify({'message': 'Invalid value for order'})
            return response, 401

        return jsonify(response)

    @classmethod
    def get_one_task(cls, id_task):
        session = open_session()

        video = session.query(Video).filter(Video.id == id_task).first()

        if video is not None:
            videos_dict = {'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value,
                           'date': video.timestamp, 'path': video.path}
            response = videos_dict
        else:
            response = jsonify({'message': 'Invalid id task'})
            return response, 401

        return jsonify(response)

    @classmethod
    def delete_one_task(cls, id_task, user_id):
        session = open_session()

        video = session.query(Video).filter(Video.id == id_task).first()

        if video is None:
            response = jsonify({'message': 'Invalid id task'})
            return response, 401

        if StatusVideo(video.status).name is StatusVideo.uploaded.name:
            response = jsonify({'message': 'Video is being processed, cannot delete it'})
            return response

        if video.user_id is not user_id:
            response = jsonify({'message': 'You are not authorized to delete it'})
            return response

        storage_client = storage.Client.from_service_account_json(SECRET_PATH)
        bucket = storage_client.bucket(BUCKET_NAME)
        edited_video = bucket.blob(f'{PATH_TO_VIDEOS}/{video.path}')
        original_video = bucket.blob(f'{PATH_TO_VIDEOS}/{video.video_id}')

        edited_video.delete()
        original_video.delete()

        session.delete(video)
        session.commit()
        session.close()
        return 'Video deleted!'
