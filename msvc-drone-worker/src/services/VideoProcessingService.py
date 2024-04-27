import base64
import cv2
import os
from decouple import config
from src.models.VideoStatus import VideoStatus


class VideoProcessingService:

    @classmethod
    def save_video(cls, file, filename):
        content = base64.b64decode(file.encode('utf-8'))
        video_path = os.environ.get('VIDEO_PATH')
        source_path = config('SOURCE_PATH')

        temp_filename = video_path + filename + '.mp4'

        with open(temp_filename, 'wb') as f:
            f.write(content)

        print(f"Video saved as {temp_filename}")

        new_video_path = video_path + filename + '-output.mp4'
        logo_path = source_path + 'logo.jpeg'

        cls.change_aspect_ratio(temp_filename, new_video_path, logo_path, logo_path, 30)

        return {
            "filename": filename,
            "status": VideoStatus.processed.name,
            "path": new_video_path
        }

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
    def delete_video(cls, video_path):
        try:
            original_video = video_path.replace('-output', '')
            print(original_video)
            if os.path.exists(original_video):
                os.remove(original_video)

            if os.path.exists(video_path):
                os.remove(video_path)
            else:
                print('Video does not exist')
        except OSError as e:
            print(f"Failed with: {e.strerror}")
            print(f"Error code: {e.code}")

        print('Video deleted successfully')
