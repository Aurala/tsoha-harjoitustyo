import sqlite3
import re

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_FILE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource(current_app.config["DATABASE_INIT_SCRIPT"]) as f:
        sql_script = f.read().decode("utf8")
        for password in re.findall(r"{{(.*?)}}", sql_script):
            sql_script = sql_script.replace(f"{{{{{password}}}}}", generate_password_hash(password))
        db.executescript(sql_script)


def populate_db():
    db = get_db()

    with current_app.open_resource(current_app.config["DATABASE_POPULATE_SCRIPT"]) as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database initialized.")


@click.command("populate-db")
def populate_db_command():
    populate_db()
    click.echo("Database populated.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
