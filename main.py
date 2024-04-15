from config import configuration
from src.initialize import init_app

configuration = configuration['development']

if __name__ == '__main__':
    init_app(configuration).run(host="0.0.0.0", port=5100)
