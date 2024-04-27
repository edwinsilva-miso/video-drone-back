import base64
import json
import os

import pika
from decouple import config
from flask import jsonify

from src.database.declarative_base import open_session
from src.models.User import User
from src.models.Video import Video, StatusVideo


class VideoUploadService:
    video_path = config('VIDEO_PATH')
    source_path = config('SOURCE_PATH')

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
    def save_video(cls, file, filename):
        # Establishing queue connection
        rabbit_url = config('RABBITMQ_URL_CONNECTION')
        url_parameters = pika.URLParameters(rabbit_url)
        connection = pika.BlockingConnection(url_parameters)
        channel = connection.channel()
        channel.queue_declare(queue='video-drone-queue')

        message = {
            'file': base64.b64encode(file.read()).decode('utf-8'),
            'filename': filename
        }

        # Send queue message
        channel.basic_publish(exchange='', routing_key='video-drone-queue', body=json.dumps(message))

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

        # Establishing queue connection
        rabbit_url = config('RABBITMQ_URL_CONNECTION')
        url_parameters = pika.URLParameters(rabbit_url)
        connection = pika.BlockingConnection(url_parameters)
        delete_channel = connection.channel()
        delete_channel.queue_declare(queue='video-drone-delete-queue')

        message = {
            'video_id': video.video_id,
            'video_path': video.path
        }
        # Send queue message
        delete_channel.basic_publish(exchange='', routing_key='video-drone-delete-queue', body=json.dumps(message))

        session.delete(video)
        session.commit()
        session.close()
        return 'Video deleted!'
