import os

from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fisjaugiasxyki:a945f138d294dd27a828141f3844484bdb3c615961102ccfe150291f17239452@ec2-52-0-67-144.compute-1.amazonaws.com:5432/df5mj5s2tjgcgn'
    
    db = SQLAlchemy(app)

    from . import db 
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    @app.route("/")
    def hello():
        return render_template('base.html')

    return app
