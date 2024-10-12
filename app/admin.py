import base64
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import db
from sqlalchemy import text

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    return redirect(url_for("admin.shop"))


@bp.route("/shop", methods=("GET", "POST"))
@login_required
def shop():

    if request.method == "POST":

        error = None

        name = request.form["name"]
        description = request.form["description"]

        if not name:
            error = "Nimi on pakollinen tieto."
        elif len(name) < 15:
            error = "Nimen on oltava vähintään 15 merkkiä."

        if error is None:
            try:
                with db.engine.begin() as connection:
                    connection.execute(
                        text("""
                        UPDATE Shops
                        SET name = :name, description = :description, is_available = TRUE
                        WHERE user_id = :user_id
                        """),
                        {
                            "name": name,
                            "description": description,
                            "user_id": g.user["user_id"]
                        }
                    )
            except db.IntegrityError:
                error = f"Kauppa nimeltä {name} on jo olemassa."
            else:
                flash("Kauppasi on nyt aktivoitu.")
                return redirect(url_for("admin.shop"))

        flash(error)

    with db.engine.connect() as connection:
        shop = connection.execute(
            text("""
                 SELECT shop_id, user_id, name, description, is_available
                 FROM Shops WHERE user_id = :user_id
                 """),
            {
                "user_id": g.user["user_id"]
            }
        ).fetchone()

    return render_template("admin/shop.html", shop=shop)


@bp.route("/products", methods=("GET", "POST"))
@login_required
def products():

    products_per_page = 8

    if request.method == "POST":
        return redirect(url_for("admin.products"))

    try:
        page = request.args.get("page", 1, type=int)
    except ValueError:
        page = 1

    with db.engine.connect() as connection:
        total_products = connection.execute(
            text("""
            SELECT COUNT(product_id)
            FROM Products
            WHERE user_id = :user_id
            """),
            {
                "user_id": g.user["user_id"]
            }
        ).fetchone()

        if total_products[0] == 0:
            flash("Sinulla ei ole tuotteita")
            render_template("admin/products.html", products=[],
                            current_page=1, total_pages=1)

        total_pages = (total_products[0] +
                       products_per_page - 1) // products_per_page

        filtered_products = connection.execute(
            text("""
            SELECT P.product_id, S.name AS shop_name, P.name, P.description, P.image_type, P.image, P.price, P.quantity
            FROM Products P
            LEFT JOIN Shops S ON P.shop_id = S.shop_id
            WHERE P.user_id = :user_id
            ORDER BY P.product_id DESC
            LIMIT :limit OFFSET :offset
            """),
            {
                "user_id": g.user["user_id"],
                "limit": products_per_page,
                "offset": (page-1)*products_per_page
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
                "name": product["name"],
                "description": product["description"],
                "price": product["price"],
                "quantity": product["quantity"],
                "shop_name": product["shop_name"],
                "image_src": image_src
            })

    return render_template("admin/products.html", products=product_list, total_products=total_products[0], current_page=page, total_pages=total_pages)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        # TODO: Update image

        # TODO: Input validation

        name = request.form.get("name", None, type=str)
        description = request.form.get("description", None, type=str)
        price = request.form.get("price", 0, type=float)
        quantity = request.form.get("quantity", 0, type=int)
        is_available = True if request.form.get("is_available") else False

        with db.engine.begin() as connection:
            connection.execute(
                text("""
                INSERT INTO Products 
                (user_id, shop_id, name, description, price, quantity, is_available)
                VALUES (:user_id, :shop_id, :name, :description, :price, :quantity, :is_available)
                """),
                {
                    "user_id": g.user["user_id"],
                    "shop_id": g.user["shop_id"],
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                    "is_available": is_available
                }
            )

        flash("Tuote lisätty.")
        return redirect(url_for("admin.products"))

    return render_template("admin/edit.html", product=[])


@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    if request.method == "POST":

        # TODO: Update image

        product_id = request.form.get("product_id", None, type=int)

        if product_id is None:
            flash("Tuotetta ei ole olemassa.")
            return redirect(url_for("admin.products"))

        with db.engine.connect() as connection:
            filtered_product = connection.execute(
                text("""
                SELECT product_id, user_id, shop_id, name, description, image_type, image, price, quantity, is_available
                FROM Products 
                WHERE product_id = :product_id AND user_id = :user_id
                """),
                {
                    "product_id": product_id,
                    "user_id": g.user["user_id"]
                }
            ).mappings().fetchone()

        if len(filtered_product) == 0:
            flash("Tuotetta ei ole olemassa.")
            return redirect(url_for("admin.products"))

        # TODO: Input validation

        name = request.form.get("name", filtered_product["name"], type=str)
        description = request.form.get(
            "description", filtered_product["description"], type=str)
        price = request.form.get(
            "price", filtered_product["price"], type=float)
        quantity = request.form.get(
            "quantity", filtered_product["quantity"], type=int)
        is_available = True if request.form.get("is_available") else False

        with db.engine.begin() as connection:
            connection.execute(
                text("""
                UPDATE Products 
                SET name = :name, description = :description, price = :price, quantity = :quantity, is_available = :is_available
                WHERE product_id = :product_id AND user_id = :user_id
                """),
                {
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                    "is_available": is_available,
                    "product_id": product_id,
                    "user_id": g.user["user_id"]
                }
            )

        flash("Tuotteen tiedot päivitetty.")
        return redirect(url_for("admin.products"))

    product_id = request.args.get("product_id", None, type=int)

    if product_id is None:
        flash("Tuotetta ei ole olemassa.")
        return redirect(url_for("admin.products"))

    with db.engine.connect() as connection:
        filtered_product = connection.execute(
            text("""
            SELECT product_id, user_id, shop_id, name, description, image_type, image, price, quantity, is_available
            FROM Products 
            WHERE product_id = :product_id AND user_id = :user_id
            """),
            {
                "product_id": product_id,
                "user_id": g.user["user_id"]
            }
        ).mappings().fetchone()

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
            "image_src": image_src
        }

    return render_template("admin/edit.html", product=product_list)


@bp.route("/sales", methods=["GET"])
@login_required
def sales():
    return render_template("admin/sales.html")
