import psycopg
from flask import current_app, g
from psycopg.rows import dict_row
import click


def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            conninfo=current_app.config['DATABASE'],
            row_factory=dict_row
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        with db.cursor() as cur:
            cur.execute(f.read().decode('utf8'))

    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
