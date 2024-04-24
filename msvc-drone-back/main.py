from config import configuration
from src.initialize import init_app
from src.consumer.VideoStatusConsumer import consume_channel

import threading

configuration = configuration['development']

if __name__ == '__main__':
    thread = threading.Thread(target=consume_channel.start_consuming)
    thread.daemon = True
    thread.start()

    init_app(configuration).run(host="0.0.0.0", port=8080)
