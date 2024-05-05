from flask import Blueprint, jsonify

main = Blueprint('external_services_blueprint', __name__)


@main.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy'
    }), 200
