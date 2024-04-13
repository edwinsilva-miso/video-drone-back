from flask import Blueprint, request, jsonify

from src.services.AuthenticationService import AuthenticationService
from src.services.VideoUploadService import VideoUploadService

main = Blueprint('video_blueprint', __name__)


@main.route('/upload', methods=['POST'])
def upload_video():
    has_access = AuthenticationService.verify_token(request.headers)

    if has_access:
        response = VideoUploadService.upload()
        return {'status': response}
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
