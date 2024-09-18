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
        "SELECT shop_id, user_id, name, description FROM Shops WHERE is_available = 1 ORDER BY shop_id DESC LIMIT 3;"
    ).fetchall()
    newest_products = db.execute(
        "SELECT product_id, user_id, name, description, price, quantity FROM Products WHERE quantity > 0 ORDER BY product_id DESC LIMIT 3;"
    ).fetchall()

    # TODO: Get TOP x shops and products
    popular_shops = []
    popular_products = []

    return render_template("ostoskeskus/index.html", newest_shops=newest_shops, newest_products=newest_products, popular_shops=popular_shops, popular_products=popular_products)


@bp.route("/search", methods=("GET", "POST"))
def search():
    return redirect(url_for("ostoskeskus.products"))


@bp.route("/products")
def products():
    return render_template("ostoskeskus/products.html")
