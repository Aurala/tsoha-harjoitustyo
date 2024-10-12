import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash
from app import db

db = SQLAlchemy()


def run_database_script(script):
    with current_app.open_resource(script) as file:
        script = file.read().decode("utf8")
        placeholders = re.findall(r"{{(.*?)}}", script)
        for placeholder in placeholders:
            hashed_password = generate_password_hash(placeholder)
            script = script.replace(f"{{{{{placeholder}}}}}", hashed_password)
        try:
            with db.engine.connect() as connection:
                connection.execute(text(script))
                db.session.commit()
            return True
        except Exception as e:
            print(f"Error executing the script: {e}")
            db.session.rollback()
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
