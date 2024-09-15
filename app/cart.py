from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/")
def index():
    return redirect(url_for("cart.view"))


@bp.route("/view", methods=("GET", "POST"))
@login_required
def view():
    return render_template("cart/view.html")
