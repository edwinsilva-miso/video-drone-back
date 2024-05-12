from flask import Flask, make_response

# Routes
from .routes import AuthRoutes
from .routes import ExternalServicesRoutes
from .routes import VideoRoutes


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    """
    Respond with a 404 and no response body.
    This will dissuade attackers pocking at random endpoints.

    :param error: any error that conducts to 404.
    :return: empty response.
    """
    return make_response('', 404)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRoutes.main, url_prefix='/msvc-back/api/oauth')
    app.register_blueprint(VideoRoutes.main, url_prefix='/msvc-back/api/videos')
    app.register_blueprint(ExternalServicesRoutes.main, url_prefix='/msvc-back/api/external')

    return app
