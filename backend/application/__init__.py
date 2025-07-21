from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import user_get
from . import card
from . import card_get
from . import org
from . import org_get
from . import org_card
from . import storage
from . import auth
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
    app.register_blueprint(card.bp)
    app.register_blueprint(card_get.bp)
    app.register_blueprint(org.bp)
    app.register_blueprint(org_get.bp)
    app.register_blueprint(org_card.bp)
    app.register_blueprint(storage.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    return app


# TODO: log card views for front end stats
# TODO: collect card org managers for Organogram
# TODO: compress photos
# TODO: design cards
# TODO: fix front end org accept card
