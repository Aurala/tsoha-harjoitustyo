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


def run_database_script(script):
    db = get_db()
    with current_app.open_resource(script) as file:
        script = file.read().decode("utf8")
        placeholders = re.findall(r"{{(.*?)}}", script)
        for placeholder in placeholders:
            hashed_password = generate_password_hash(placeholder)
            script = script.replace(f"{{{{{placeholder}}}}}", hashed_password)
        try:
            db.executescript(script)
            db.commit()
        except Exception as e:
            print(f"Error executing the script: {e}")


def init_db():
    run_database_script(current_app.config["DATABASE_INIT_SCRIPT"])


def populate_db():
    run_database_script(current_app.config["DATABASE_POPULATE_SCRIPT"])


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
