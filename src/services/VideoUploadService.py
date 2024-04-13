from decouple import config

# from src.database.declarative_base import Session
# from src.models.User import User


class VideoUploadService:
    video_path = config('VIDEO_PATH')

    @classmethod
    def upload(cls):
        """
        Implement here the video upload process
        """
        # These lines are a test for query videos for an user
        # user = Session.query(User).filter_by(id=1).first()
        # print(user.videos)
        return 'Video uploaded!'
