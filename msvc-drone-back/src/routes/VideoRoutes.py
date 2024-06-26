import uuid

from flask import Blueprint, request, jsonify

from src.services.AuthenticationService import AuthenticationService
from src.services.VideoUploadService import VideoUploadService

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

        random_name = uuid.uuid4().__str__()  # + '.mp4'

        user_id = AuthenticationService.get_id_from_token(request.headers)
        response = VideoUploadService.upload(description, random_name, user_id)

        if not response:
            return jsonify({"success": False}), 400

        VideoUploadService.save_video_to_gcs(video_file, random_name)
        return response, 201
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/tasks', methods=['GET'])
def get_tasks():
    has_access = AuthenticationService.verify_token(request.headers)

    if has_access:
        order = request.args.get('order')
        maxim = request.args.get('max')

        user_id = AuthenticationService.get_id_from_token(request.headers)
        response = VideoUploadService.get_all_tasks(user_id=user_id, order=order, maxim=maxim)

        return response
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/tasks/<int:id_task>', methods=['GET'])
def get_one_tasks(id_task):
    has_access = AuthenticationService.verify_token(request.headers)

    if has_access:
        response = VideoUploadService.get_one_task(id_task=id_task)
        return response
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/tasks/<int:id_task>', methods=['DELETE'])
def delete_one_tasks(id_task):
    has_access = AuthenticationService.verify_token(request.headers)

    if has_access:
        user_id = AuthenticationService.get_id_from_token(request.headers)
        response = VideoUploadService.delete_one_task(id_task=id_task, user_id=user_id)
        return response
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
