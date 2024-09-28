from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint("cart", __name__, url_prefix="/cart")


@bp.route("/")
def index():
    return redirect(url_for("cart.view"))


@bp.route("/view", methods=["GET"])
@login_required
def view():
    return render_template("cart/view.html")


@bp.route("/add/<int:product_id>", methods=["GET"])
@login_required
def add(product_id):

    if "cart" not in session:
        session["cart"] = {}

    error = None

    db = get_db()
    product = db.execute(
        "SELECT quantity FROM Products WHERE product_id=?;",
        (product_id,)
    ).fetchone()

    if product is None:
        flash(f"Tuotetta {product_id} ei ole olemassa.")
    elif product["quantity"] < 1:
        flash(f"Tuotetta {product_id} ei ole saatavilla.")
    else:
        session["cart"]["_" + str(product_id)] = session["cart"].get("_" + str(product_id), 0) + 1
        flash(f"Tuote {product_id} lisätty ostoskoriin.")

    return redirect(url_for("cart.view"))


@bp.route("/remove/<int:product_id>", methods=["GET"])
@login_required
def remove(product_id):

    if "cart" not in session:
        session["cart"] = {}

    current_amount = session["cart"].get("_" + str(product_id), 0)

    if current_amount > 0:
        current_amount -= 1

        if current_amount > 0:
            session["cart"]["_" + str(product_id)] = current_amount
            flash(f"Tuotteen {product_id} määrä vähennetty.")
        else:
            session["cart"].pop("_" + str(product_id), None)
            flash(f"Tuote {product_id} poistettu ostoskorista.")
    else:
        flash(f"Tuotetta {product_id} ei ole ostoskorissa.")

    return redirect(url_for("cart.view"))
