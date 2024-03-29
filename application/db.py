import psycopg2
import os
import click 
from flask import current_app, g
from flask.cli import with_appcontext
import urllib.parse as urlparse

def get_db():
    if 'db' not in g:
        dbname = current_app.config['SQLALCHEMY_DATABASE_URI'] 
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        g.db = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                    )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    f = current_app.open_resource("sql/database.sql")
    sql_code = f.read().decode("ascii")
    cur = db.cursor()
    cur.execute(sql_code)
    cur.close()
    db.commit()
    close_db()        

@click.command('initdb', help="initialise the database")
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
