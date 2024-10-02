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


@bp.route("/shops", methods=["GET"])
def shops():
    return render_template("ostoskeskus/shops.html")


@bp.route("/products", methods=["GET"])
def products():

    products_per_page = 8

    try:
        page = request.args.get("page", 1, type=int)
    except ValueError:
        page = 1
    search_term = request.args.get("search", "", type=str)
    try:
        shop = request.args.get("shop", None, type=int)
    except ValueError:
        shop = None

    db = get_db()

    total_products = db.execute("SELECT COUNT(product_id) FROM Products WHERE (name LIKE ? OR description LIKE ?) AND (Products.shop_id = ? OR ? IS NULL) AND is_available=1;",
                                ("%" + search_term + "%", "%" +
                                 search_term + "%", shop, shop)
                                ).fetchone()

    if total_products[0] == 0:
        flash("Tuotteita ei löytynyt")
        render_template("ostoskeskus/products.html",
                        products=[], current_page=1, total_pages=1)

    total_pages = (total_products[0] +
                   products_per_page - 1) // products_per_page

    filtered_products = db.execute("SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE (name LIKE ? OR description LIKE ?) AND (Products.shop_id = ? OR ? IS NULL) AND is_available=1 ORDER BY product_id DESC LIMIT ? OFFSET ?;",
                                   ("%" + search_term + "%", "%" + search_term + "%", shop,
                                    shop, products_per_page, (page-1)*products_per_page)
                                   ).fetchall()

    return render_template("ostoskeskus/products.html", products=filtered_products, current_page=page, total_pages=total_pages)
