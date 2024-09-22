import sqlite3
import re

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_FILE"],
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
            return True
        except Exception as e:
            print(f"Error executing the script: {e}")
            return False


def init_db():
    return run_database_script(current_app.config["DATABASE_INIT_SCRIPT"])


def populate_db():
    return run_database_script(current_app.config["DATABASE_POPULATE_SCRIPT"])


@click.command("init-db")
def init_db_command():
    if init_db():
        click.echo("Database initialized.")
        return

    click.echo("Database initialization failed.")


@click.command("populate-db")
def populate_db_command():
    if populate_db():
        click.echo("Database populated.")
        return

    click.echo("Database population failed.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)
