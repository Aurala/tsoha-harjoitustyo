import base64
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from sqlalchemy import text
from app.auth import login_required
from app.db import db

bp = Blueprint("cart", __name__, url_prefix="/cart")


def get_cart():

    if "cart" not in session:
        session["cart"] = {}

    if len(session["cart"]) == 0:
        return []

    # TODO: Validate product IDs

    product_ids = [int(key[1:]) for key in session["cart"].keys()]

    with db.engine.connect() as connection:
        filtered_products = connection.execute(
            text("""
            SELECT P.product_id, P.user_id, P.shop_id, P.name, P.description, P.image_type, P.image, P.price, P.quantity, P.is_available, S.name AS shop_name
            FROM Products P
            LEFT JOIN Shops S ON P.shop_id = S.shop_id
            WHERE P.product_id = ANY(:product_ids)
            """),
            {
                "product_ids": product_ids
            }
        ).mappings().fetchall()

        product_list = []
        for product in filtered_products:
            if product["image"]:
                image_data = base64.b64encode(product["image"]).decode("utf-8")
                image_src = f"{product['image_type']},{image_data}"
            else:
                image_src = None

            product_list.append({
                "product_id": product["product_id"],
                "user_id": product["user_id"],
                "shop_id": product["shop_id"],
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "quantity": product["quantity"],
                "image_src": image_src,
                "is_available": product["is_available"],
                "shop_name": product["shop_name"],
            })

    return product_list


@bp.route("/")
def index():
    return redirect(url_for("cart.view"))


@bp.route("/view", methods=["GET"])
@login_required
def view():
    products = get_cart()
    return render_template("cart/view.html", products=products)


@bp.route("/order", methods=["POST"])
@login_required
def order():

    products = get_cart()

    # TODO: Manage quantities

    with db.engine.begin() as connection:
        result = connection.execute(
            text("""
            INSERT INTO Orders (user_id, ordered)
            VALUES (:user_id, :ordered)
            RETURNING order_id
            """),
            {
                "user_id": g.user["user_id"],
                "ordered": datetime.datetime.now()
            }
        ).mappings().fetchone()
        order_id = result["order_id"]

        for product in products:
            connection.execute(
                text("""
                INSERT INTO OrderedProducts (order_id, product_id, quantity, price)
                VALUES (:order_id, :product_id, :quantity, :price)
                """),
                {
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": session["cart"]["_" + str(product["product_id"])],
                    "price": product["price"]
                }
            )

    session["cart"] = {}
    flash("Tilaus onnistui!")

    return render_template("cart/receipt.html")


@bp.route("/add/<int:product_id>", methods=["GET"])
@login_required
def add(product_id):

    if "cart" not in session:
        session["cart"] = {}

    with db.engine.connect() as connection:
        product = connection.execute(
            text("""
            SELECT name, quantity
            FROM Products
            WHERE product_id = :product_id
            """),
            {
                "product_id": product_id
            }
        ).mappings().fetchone()

    if product is None:
        flash(f"Tuotetta {product_id} ei ole olemassa.")
    elif product["quantity"] < 1:
        flash(f"Tuotetta {product['name']} ei ole saatavilla.")
    else:
        session["cart"]["_" +
                        str(product_id)] = session["cart"].get("_" + str(product_id), 0) + 1
        flash(f"Tuote {product['name']} lisätty ostoskoriin.")

    return redirect(url_for("cart.view"))


@bp.route("/remove/<int:product_id>", methods=["GET"])
@login_required
def remove(product_id):

    if "cart" not in session:
        session["cart"] = {}

    with db.engine.connect() as connection:
        product = connection.execute(
            text("""
            SELECT name, quantity
            FROM Products
            WHERE product_id = :product_id
            """),
            {
                "product_id": product_id
            }
        ).mappings().fetchone()

    current_amount = session["cart"].get("_" + str(product_id), 0)

    if current_amount > 0:
        current_amount -= 1
        if current_amount > 0:
            session["cart"]["_" + str(product_id)] = current_amount
            flash(
                f"Tuotteen {product['name']} määrää vähennetty ostoskorissa.")
        else:
            session["cart"].pop("_" + str(product_id), None)
            flash(f"Tuote {product['name']} poistettu ostoskorista.")
    else:
        flash(f"Tuotetta {product_id} ei ole ostoskorissa.")

    return redirect(url_for("cart.view"))
