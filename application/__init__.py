import os
import psycopg2
from flask import Flask, render_template, request

def create_app():
    app = Flask(__name__)
    DATABASE_URL = os.environ['DATABASE_URL'] = 'postgres://fisjaugiasxyki:a945f138d294dd27a828141f3844484bdb3c615961102ccfe150291f17239452@ec2-52-0-67-144.compute-1.amazonaws.com:5432/df5mj5s2tjgcgn'
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    from . import db 
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    @app.route("/")
    def hello():
        return render_template('base.html')

    return app
