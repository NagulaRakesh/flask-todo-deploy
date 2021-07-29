import os
import psycopg2
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    DATABASE_DEFAULT = 'TODO'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DATABASE_DEFAULT)
    db = SQLAlchemy(app)
    
    from . import db 
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    @app.route("/")
    def hello():
        return render_template('base.html')

    return app
