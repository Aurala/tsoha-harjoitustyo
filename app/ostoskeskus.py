import base64
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from sqlalchemy import text
from app.db import db

bp = Blueprint("ostoskeskus", __name__)


@bp.route("/")
def index():
    with db.engine.connect() as connection:
        newest_shops = connection.execute(
            text("""
            SELECT shop_id, user_id, name, description
            FROM Shops
            WHERE is_available=TRUE
            ORDER BY shop_id DESC
            LIMIT 3
            """)
        ).mappings().fetchall()

        newest_products = connection.execute(
            text("""
            SELECT P.product_id, P.name, P.description, P.price, P.quantity, S.name AS shop_name
            FROM Products P
            LEFT JOIN Shops S ON P.shop_id = S.shop_id
            WHERE P.is_available = TRUE AND p.quantity > 0
            ORDER BY P.product_id DESC
            LIMIT 3
            """)
        ).mappings().fetchall()

        popular_products = connection.execute(
            text("""
            SELECT P.product_id, P.name, P.description, SUM(OP.quantity) AS total
            FROM OrderedProducts OP
            INNER JOIN Products P ON OP.product_id = P.product_id
            WHERE P.is_available = TRUE
            GROUP BY P.product_id, P.name, P.description
            ORDER BY total DESC
            LIMIT 3
            """)
        ).mappings().fetchall()

        popular_shops = connection.execute(
            text("""
            SELECT S.shop_id, S.name, S.description, SUM(OP.quantity) AS total
            FROM Shops S
            INNER JOIN Products P ON S.shop_id = P.shop_id
            INNER JOIN OrderedProducts OP ON P.product_id = OP.product_id
            WHERE P.is_available = TRUE
            GROUP BY S.shop_id, S.name
            ORDER BY total DESC
            LIMIT 3
            """)
        ).mappings().fetchall()

    return render_template("ostoskeskus/index.html",
                           newest_shops=newest_shops,
                           newest_products=newest_products,
                           popular_shops=popular_shops,
                           popular_products=popular_products)


@bp.route("/shops", methods=["GET"])
def shops():
    with db.engine.connect() as connection:
        random_shops = connection.execute(
            text("""
            SELECT shop_id, name, description
            FROM Shops
            ORDER BY random()
            LIMIT 4
            """)
        ).mappings().fetchall()

    return render_template("ostoskeskus/shops.html",
                           shops=random_shops)


@bp.route("/product/<int:product_id>", methods=["GET"])
def product(product_id):
    with db.engine.connect() as connection:
        filtered_product = connection.execute(
            text("""
            SELECT P.product_id, P.name, P.description, P.image_type, P.image, P.price, P.quantity, P.is_available, S.name AS shop_name
            FROM Products P
            LEFT JOIN Shops S ON P.shop_id = S.shop_id
            WHERE P.product_id = :product_id AND P.is_available = TRUE
            """),
            {
                "product_id": product_id
            }
        ).mappings().fetchone()

    if filtered_product is None:
        flash("Tuotetta ei löytynyt.")
        return redirect(url_for("products"))

    if filtered_product["image"]:
        image_data = base64.b64encode(
            filtered_product["image"]).decode("utf-8")
        image_src = f"{filtered_product['image_type']},{image_data}"
    else:
        image_src = None

    product_list = {
        "product_id": filtered_product["product_id"],
        "name": filtered_product["name"],
        "description": filtered_product["description"],
        "price": filtered_product["price"],
        "quantity": filtered_product["quantity"],
        "shop_name": filtered_product["shop_name"],
        "image_src": image_src,
        "is_available": filtered_product["is_available"]
    }

    return render_template("ostoskeskus/products.html",
                           products=[product_list],
                           current_page=1,
                           total_pages=1)


@bp.route("/products", methods=["GET", "POST"])
def products():

    products_per_page = 8

    try:
        page = request.args.get(
            "page") or request.form.get("page", 1, type=int)
    except ValueError:
        page = 1
    search_term = request.args.get(
        "search") or request.form.get("search", "", type=str)
    try:
        shop_id = request.args.get("shop_id") or request.form.get(
            "shop_id", None, type=int)
    except ValueError:
        shop_id = None

    with db.engine.connect() as connection:
        total_products = connection.execute(
            text("""
            SELECT COUNT(product_id)
            FROM Products
            WHERE (name LIKE :search_term OR description LIKE :search_term) AND (shop_id = :shop_id OR :shop_id IS NULL) AND is_available = TRUE AND quantity > 0
            """),
            {
                "search_term": "%" + search_term + "%",
                "shop_id": shop_id
            }
        ).fetchone()

        if total_products[0] == 0:
            flash("Tuotteita ei löytynyt")
            render_template("ostoskeskus/products.html",
                            products=[], current_page=1, total_pages=1)

        total_pages = (total_products[0] +
                       products_per_page - 1) // products_per_page

        filtered_products = connection.execute(
            text("""
            SELECT P.product_id, P.name, P.description, P.image_type, P.image, P.price, P.quantity, S.name AS shop_name
            FROM Products P
            LEFT JOIN Shops S ON P.shop_id = S.shop_id
            WHERE (P.name LIKE :search_term OR P.description LIKE :search_term)
            AND (P.shop_id = :shop_id OR :shop_id IS NULL)
            AND P.is_available = TRUE AND P.quantity > 0
            ORDER BY P.product_id DESC
            LIMIT :limit OFFSET :offset
            """),
            {
                "search_term": "%" + search_term + "%",
                "shop_id": shop_id,
                "limit": products_per_page,
                "offset": (page-1)*products_per_page
            }
        ).mappings().fetchall()

        product_list = []
        for prod in filtered_products:
            if prod["image"]:
                image_data = base64.b64encode(prod["image"]).decode("utf-8")
                image_src = f"{prod['image_type']},{image_data}"
            else:
                image_src = None

            product_list.append({
                "product_id": prod["product_id"],
                "name": prod["name"],
                "description": prod["description"],
                "price": prod["price"],
                "quantity": prod["quantity"],
                "shop_name": prod["shop_name"],
                "image_src": image_src
            })

    return render_template("ostoskeskus/products.html",
                           products=product_list,
                           current_page=page,
                           total_pages=total_pages)
