import psycopg
from flask import current_app, g
from psycopg.rows import dict_row

def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            conninfo=current_app.config['DATABASE'],
            row_factory=dict_row
        )

    return g.db

def close_db(e=None):
    db=g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
        

