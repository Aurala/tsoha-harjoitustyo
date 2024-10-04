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
    popular_products = db.execute(
        "SELECT P.product_id, P.name, P.description, SUM(OP.quantity) AS total FROM OrderedProducts OP INNER JOIN products P ON OP.product_id = P.product_id GROUP BY OP.product_id, P.name ORDER BY total DESC LIMIT 3;"
    ).fetchall()
    popular_shops = db.execute(
        "SELECT S.shop_id, S.name, S.description, SUM(OP.quantity) AS total FROM Shops S INNER JOIN Products P ON S.shop_id = P.shop_id INNER JOIN OrderedProducts OP ON P.product_id = OP.product_id GROUP BY S.shop_id, S.name ORDER BY total  DESC LIMIT 3;"
    ).fetchall()

    return render_template("ostoskeskus/index.html", newest_shops=newest_shops, newest_products=newest_products, popular_shops=popular_shops, popular_products=popular_products)


@bp.route("/shops", methods=["GET"])
def shops():
    return render_template("ostoskeskus/shops.html")


@bp.route("/product/<int:product_id>", methods=["GET"])
def product(product_id):
    db = get_db()

    product = db.execute(
        "SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE product_id=? AND is_available=1;",
        (product_id,)
    ).fetchone()

    if product is None:
        flash("Tuotetta ei löytynyt.")
        return redirect(url_for("products"))

    return render_template("ostoskeskus/products.html", products=[product], current_page=1, total_pages=1)


@bp.route("/products", methods=["GET"])
def products():

    products_per_page = 8

    try:
        page = request.args.get("page", 1, type=int)
    except ValueError:
        page = 1
    search_term = request.args.get("search", "", type=str)
    try:
        shop_id = request.args.get("shop_id", None, type=int)
    except ValueError:
        shop_id = None

    db = get_db()

    total_products = db.execute("SELECT COUNT(product_id) FROM Products WHERE (name LIKE ? OR description LIKE ?) AND (Products.shop_id = ? OR ? IS NULL) AND is_available=1;",
                                ("%" + search_term + "%", "%" +
                                 search_term + "%", shop_id, shop_id)
                                ).fetchone()

    if total_products[0] == 0:
        flash("Tuotteita ei löytynyt")
        render_template("ostoskeskus/products.html",
                        products=[], current_page=1, total_pages=1)

    total_pages = (total_products[0] +
                   products_per_page - 1) // products_per_page

    filtered_products = db.execute("SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE (name LIKE ? OR description LIKE ?) AND (Products.shop_id = ? OR ? IS NULL) AND is_available=1 ORDER BY product_id DESC LIMIT ? OFFSET ?;",
                                   ("%" + search_term + "%", "%" + search_term + "%", shop_id,
                                    shop_id, products_per_page, (page-1)*products_per_page)
                                   ).fetchall()

    return render_template("ostoskeskus/products.html", products=filtered_products, current_page=page, total_pages=total_pages)
