"""Define App Factory function to create the Flask App"""

import os
from flask import Flask, jsonify

# Configuration
from abitly.config import ProductionConfig, TestingConfig, DevelopmentConfig

# Database
from abitly.db import db_session, init_db

# Blueprints
from abitly.services.link.bp import link

# Utils
from abitly.utils import format_exception


def create_app():
    """Configure the Flask App"""

    app = Flask(__name__, instance_relative_config=True)
    flask_env = os.getenv('FLASK_ENV')

    # Use Config Classes per FLASK_ENV
    if flask_env == 'production':
        app.config.from_object(ProductionConfig)
    elif flask_env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize DB
    init_db()

    # Remove DB Session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Routes
    @app.route('/')
    def index():
        return jsonify(statusCode=200,
                       status='OK',
                       message='ABitly is running')

    # Register Blueprints
    app.register_blueprint(link)

    # Error Handlers
    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def method_not_allowed(exception):
        statusCode, status, error_message = format_exception(exception)

        return jsonify(statusCode=statusCode,
                       status=status,
                       errorMessage=error_message
                       ), statusCode

    return app
