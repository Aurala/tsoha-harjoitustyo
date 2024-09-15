from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    csrf.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import ostoskeskus
    app.register_blueprint(ostoskeskus.bp)
    app.add_url_rule("/", endpoint="index")

    from . import db
    db.init_app(app)

    return app
