import os

import pika
from decouple import config
from flask import jsonify

from src.database.declarative_base import Session
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
        user = Session.query(User).filter_by(id=user_id).first()

        if description:
            new_video = Video(
                description=description,
                video_id=video_name,
                path='',
                user_id=user.id,
                status=StatusVideo.uploaded
            )
            Session.add(new_video)
            Session.commit()
            return 'Video uploaded!'

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
            'file': file,
            'filename': filename
        }

        # Send queue message
        channel.basic_publish(exchange='', routing_key='video-drone-queue', body=message)

        return 'Video sent to process'

    @classmethod
    def update_video_process(cls, filename, status, new_video_path):
        video_processed = Session.query(Video).filter(Video.video_id == filename).one_or_none()
        if video_processed:
            video_processed.status = status
            video_processed.path = new_video_path,
            Session.commit()

    @classmethod
    def get_all_tasks(cls, user_id, order, maxim=None):

        if order == '0':
            videos = Session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.asc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value,
                            'date': video.timestamp} for video in videos]
            response = videos_dict

        elif order == '1':
            videos = Session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.desc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value,
                            'date': video.timestamp} for video in videos]
            response = videos_dict
        else:
            response = jsonify({'message': 'Invalid value for order'})
            return response, 401

        return jsonify(response)

    @classmethod
    def get_one_task(cls, id_task):

        video = Session.query(Video).filter(Video.id == id_task).first()

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
        video_path = config('VIDEO_PATH')
        video = Session.query(Video).filter(Video.id == id_task).first()

        if video is None:
            response = jsonify({'message': 'Invalid id task'})
            return response, 401

        if StatusVideo(video.status).name is StatusVideo.uploaded.name:
            response = jsonify({'message': 'Video is being processed, cannot delete it'})
            return response

        if video.user_id is not user_id:
            response = jsonify({'message': 'You are not authorized to delete it'})
            return response

        if os.path.exists(video.path):
            os.remove(video.path)
        else:
            response = jsonify({'message': 'Video does not exist'})
            return response

        original_video_path = video_path + video.video_id + ".mp4"
        if os.path.exists(original_video_path):
            os.remove(original_video_path)
        else:
            response = jsonify({'message': 'Video does not exist'})
            return response

        Session.delete(video)
        Session.commit()
        return 'Video deleted!'
