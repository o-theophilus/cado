from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import user_get
from . import organization
from . import organization_get
from . import user_organization
from . import storage
from . import account
from . import admin


def create_app(conf=None):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    if conf:
        app.config.from_pyfile(conf)
    CORS(app)

    @app.route("/")
    def index():

        return jsonify({
            "status": 200,
            "message": "Welcome to URLinks"
        })

    app.register_blueprint(api.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(organization.bp)
    app.register_blueprint(organization_get.bp)
    app.register_blueprint(user_organization.bp)
    app.register_blueprint(storage.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(admin.bp)

    return app
