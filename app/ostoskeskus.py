from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.db import get_db

bp = Blueprint("ostoskeskus", __name__)


@bp.route("/")
def index():
    db = get_db()
    newest_shops = db.execute(
        "SELECT shop_id, user_id, name, description FROM Shops WHERE is_available=1 ORDER BY shop_id DESC LIMIT 3;"
    ).fetchall()
    newest_products = db.execute(
        "SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, price, quantity FROM Products WHERE is_available=1 ORDER BY product_id DESC LIMIT 3;"
    ).fetchall()

    # TODO: Get TOP x shops and products
    popular_shops = []
    popular_products = []

    return render_template("ostoskeskus/index.html", newest_shops=newest_shops, newest_products=newest_products, popular_shops=popular_shops, popular_products=popular_products)


@bp.route("/products", methods=("GET", "POST"))
def products():
    if request.method == "POST":
        search_term = request.form["search"]
        if search_term is None:
            return redirect(url_for("ostoskeskus.index"))

        db = get_db()
        filtered_products = db.execute(
            "SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE is_available=1 ORDER BY product_id DESC LIMIT 10;"
        ).fetchall()
        return render_template("ostoskeskus/products.html", products=filtered_products)

    db = get_db()
    all_products = db.execute(
        "SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE is_available=1 ORDER BY product_id DESC LIMIT 10;",
    ).fetchall()

    return render_template("ostoskeskus/products.html", products=all_products)
