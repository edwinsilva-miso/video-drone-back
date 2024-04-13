from decouple import config
from flask import jsonify

from src.models.Video import Video, StatusVideo
from src.models.User import User
from src.database.declarative_base import Session
import cv2


class VideoUploadService:
    video_path = config('VIDEO_PATH')
    source_path = config('SOURCE_PATH')

    @classmethod
    def upload(cls, description, video_name, user_id):
        """
        Implement here the video upload process
        """
        video_path = config('VIDEO_PATH')

        # These lines are a test for query videos for an user
        user = Session.query(User).filter_by(id=user_id).first()

        if description:
            new_video = Video(
                description=description,
                path=video_path + video_name + '-output.mp4',
                user_id=user.id,
                status=StatusVideo.uploaded
            )
            Session.add(new_video)
            Session.commit()
            return 'Video uploaded!'

        return False

    @classmethod
    async def save_video(cls, file, filename):
        video_path = config('VIDEO_PATH')
        source_path = config('SOURCE_PATH')

        temp_filename = video_path + filename + '.mp4'

        with open(temp_filename, 'wb') as f:
            while True:
                chunk = file.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Video saved as {temp_filename}")

        new_name = video_path + filename + '-output.mp4'
        logo_path = source_path + 'logo.jpeg'

        cls.change_aspect_ratio(temp_filename, new_name, logo_path, logo_path, 30)

        video_processed = Session.query(Video).filter(Video.path == new_name).one_or_none()
        if video_processed:
            video_processed.status = StatusVideo.processed
            Session.commit()

    @classmethod
    def change_aspect_ratio(cls, video_path, output_path, start_image_path, end_image_path, num_frames):
        # Read the video file
        cap = cv2.VideoCapture(video_path)

        # Get the video's width and height
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Calculate the new width and height for a 16:9 aspect ratio
        new_width = int(height * 16 / 9)
        new_height = height

        # Get the original frame rate
        frame_rate = cap.get(cv2.CAP_PROP_FPS)

        # Create a video writer object with the original frame rate
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, (new_width, new_height))

        # Read start image
        start_image = cv2.imread(start_image_path)
        start_image = cv2.resize(start_image, (new_width, new_height))

        # Read end image
        end_image = cv2.imread(end_image_path)
        end_image = cv2.resize(end_image, (new_width, new_height))

        # Write start frames
        for _ in range(num_frames):
            out.write(start_image)

        # Loop over the frames in the video
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # If the frame is empty, break out of the loop
            if not ret:
                break

            # Resize the frame to the new aspect ratio
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Write the resized frame to the output video
            out.write(resized_frame)

        # Write end frames
        for _ in range(num_frames):
            out.write(end_image)

        # Release the video capture and writer objects
        cap.release()
        out.release()

    @classmethod
    def get_all_tasks(cls, user_id, order, maxim=None):

        if order == '0':
            videos = Session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.asc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value, 'date': video.timestamp} for video in videos]
            response = videos_dict

        elif order == '1':
            videos = Session.query(Video).filter(Video.user_id == user_id).order_by(Video.id.desc()).limit(maxim).all()
            videos_dict = [{'id': video.id, 'description': video.description, 'status': StatusVideo(video.status).value, 'date': video.timestamp} for video in videos]
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
