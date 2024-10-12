from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from . import auth
from . import admin
from . import cart
from . import ostoskeskus
from .db import db, init_db_command, populate_db_command

csrf = CSRFProtect()


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    csrf.init_app(app)

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(ostoskeskus.bp)

    app.add_url_rule("/", endpoint="index")

    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_db_command)

    return app
