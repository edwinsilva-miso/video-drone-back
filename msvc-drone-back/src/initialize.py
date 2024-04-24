from flask import Flask

# Routes
from .routes import AuthRoutes
from .routes import VideoRoutes


app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix='/oauth')
    app.register_blueprint(VideoRoutes.main, url_prefix='/api/videos')

    return app
