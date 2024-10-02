from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint("cart", __name__, url_prefix="/cart")


def get_cart():

    if "cart" not in session:
        session["cart"] = {}

    if len(session["cart"]) == 0:
        return []

    # TODO: Validate product IDs

    product_ids = [int(key.replace("_", "")) for key in session["cart"].keys()]
    placeholders = ', '.join('?' * len(product_ids))

    db = get_db()

    filtered_products = db.execute(f"SELECT product_id, user_id, shop_id, name, description, image, price, quantity, is_available FROM Products WHERE product_id IN ({placeholders});",
                                      product_ids).fetchall()

    return filtered_products


@bp.route("/")
def index():
    return redirect(url_for("cart.view"))


@bp.route("/view", methods=["GET"])
@login_required
def view():
    products = get_cart()
    return render_template("cart/view.html", products=products)


@bp.route("/order", methods=["GET"])
@login_required
def order():
    return


@bp.route("/add/<int:product_id>", methods=["GET"])
@login_required
def add(product_id):

    if "cart" not in session:
        session["cart"] = {}

    db = get_db()
    product = db.execute(
        "SELECT name, quantity FROM Products WHERE product_id=?;",
        (product_id,)
    ).fetchone()

    if product is None:
        flash(f"Tuotetta {product_id} ei ole olemassa.")
    elif product["quantity"] < 1:
        flash(f"Tuotetta '{product['name']}' ei ole saatavilla.")
    else:
        # Numeric dictionary keys are not allowed, using "_" as a prefix
        session["cart"]["_" + str(product_id)] = session["cart"].get("_" + str(product_id), 0) + 1
        flash(f"Tuote '{product["name"]}' lisätty ostoskoriin.")

    return redirect(url_for("cart.view"))


@bp.route("/remove/<int:product_id>", methods=["GET"])
@login_required
def remove(product_id):

    if "cart" not in session:
        session["cart"] = {}

    db = get_db()
    product = db.execute(
        "SELECT name, quantity FROM Products WHERE product_id=?;",
        (product_id,)
    ).fetchone()

    current_amount = session["cart"].get("_" + str(product_id), 0)

    if current_amount > 0:
        current_amount -= 1
        if current_amount > 0:
            session["cart"]["_" + str(product_id)] = current_amount
            flash(f"Tuotteen '{product["name"]}' määrää vähennetty.")
        else:
            session["cart"].pop("_" + str(product_id), None)
            flash(f"Tuote '{product['name']}' poistettu ostoskorista.")
    else:
        flash(f"Tuotetta {product_id} ei ole ostoskorissa.")

    return redirect(url_for("cart.view"))
