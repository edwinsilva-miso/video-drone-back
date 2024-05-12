from flask import Flask, make_response

from src.routes import ExternalServicesRoutes

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


def provide_app():
    # Configuration
    app.register_blueprint(ExternalServicesRoutes.main, url_prefix='/msvc-back/api/external')

    return app
