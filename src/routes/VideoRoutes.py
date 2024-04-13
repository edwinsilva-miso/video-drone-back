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
        response = VideoUploadService.upload(description, random_name, '1')

        asyncio.run(VideoUploadService.save_video(video_file, random_name))  # Use asyncio.run() to execute the coroutine
        return {'status': response}
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
