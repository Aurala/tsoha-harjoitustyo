from flask import Flask


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    from . import auth
    app.register_blueprint(auth.bp)

    from . import ostoskeskus
    app.register_blueprint(ostoskeskus.bp)
    app.add_url_rule("/", endpoint="index")

    from . import db
    db.init_app(app)

    return app
