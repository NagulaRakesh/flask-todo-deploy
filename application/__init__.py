import os

from flask import Flask, render_template, request


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE="DATABASE_URL"
    )

    from . import db 
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    @app.route("/")
    def hello():
        return render_template('base.html')

    return app
