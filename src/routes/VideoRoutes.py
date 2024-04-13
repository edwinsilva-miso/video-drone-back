from flask import Blueprint, request, jsonify

from src.services.AuthenticationService import AuthenticationService
from src.services.VideoUploadService import VideoUploadService
import uuid
import asyncio

main = Blueprint('video_blueprint', __name__)


@main.route('/upload', methods=['POST'])
def upload_video():
    has_access = AuthenticationService.verify_token(request.headers)

    if has_access:

        if 'video' not in request.files:
            return "No video file provided", 400

        video_file = request.files['video']
        if video_file.filename == '':
            return "No selected file", 400

        description = request.values["description"]

        random_name = uuid.uuid4().__str__()

        user_id = AuthenticationService.get_id_from_token(request.headers)
        response = VideoUploadService.upload(description, random_name, user_id)

        asyncio.run(VideoUploadService.save_video(video_file, random_name))
        return {'status': response}
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/tasks', methods=['GET'])
def get_tasks():

    print("Hola")
    has_access = AuthenticationService.verify_token(request.headers)

    order = request.args.get('order')
    maxim = request.args.get('max')

    if has_access:
        user_id = AuthenticationService.get_id_from_token(request.headers)
        response = VideoUploadService.get_all_tasks(user_id=user_id, order=order, maxim=maxim)

        return response
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
