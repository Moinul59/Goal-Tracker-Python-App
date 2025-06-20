import click
from flask import Flask
from flaskr.models import db


@click.command("init-db")
def init_db_command():
    """Create all database tables."""
    db.create_all()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    app.cli.add_command(init_db_command)
