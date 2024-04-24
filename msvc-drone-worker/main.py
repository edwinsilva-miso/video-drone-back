from config import configuration
from src.initialize import init_app
from src.tasks import VideoWorkerConsumer

import threading

configuration = configuration['development']


if __name__ == '__main__':
    thread = threading.Thread(target=VideoWorkerConsumer.save_video_task)
    thread.daemon = True
    thread.start()

    init_app(configuration).run(host="0.0.0.0", port=8081)
