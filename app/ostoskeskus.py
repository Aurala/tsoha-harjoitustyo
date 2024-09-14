from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint("ostoskeskus", __name__)


@bp.route("/")
def index():
    return f"Indeksi toimii"


@bp.route("/hello")
def hello():
    return f"Hello, World!"
