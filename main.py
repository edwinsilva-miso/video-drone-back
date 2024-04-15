from config import configuration
from src.initialize import init_app

configuration = configuration['development']
app = init_app(configuration)

if __name__ == '__main__':
    app.run(port=8080)
