import base64
from io import BytesIO
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from PIL import Image
from werkzeug.utils import secure_filename
from sqlalchemy import text
from app.auth import login_required
from app.db import db

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
        elif len(name) < 15 or len(name) > 50:
            error = "Nimen on oltava 15-50 merkkiä."

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
        filtered_shop = connection.execute(
            text("""
                 SELECT shop_id, user_id, name, description, is_available
                 FROM Shops WHERE user_id = :user_id
                 """),
            {
                "user_id": g.user["user_id"]
            }
        ).fetchone()

    return render_template("admin/shop.html",
                           shop=filtered_shop)


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
            SELECT P.product_id, S.name AS shop_name, P.name, P.description, P.image_type, P.image, P.price, P.quantity, P.is_available
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
                "image_src": image_src,
                "is_available": product["is_available"]
            })

    return render_template("admin/products.html",
                           products=product_list,
                           total_products=total_products[0],
                           current_page=page,
                           total_pages=total_pages)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        error = None

        name = request.form.get("name", None, type=str)
        description = request.form.get("description", None, type=str)
        price = request.form.get("price", 0, type=float)
        quantity = request.form.get("quantity", 0, type=int)
        is_available = bool(request.form.get("is_available"))

        if not name or len(name) < 5 or len(name) > 25:
            error = "Nimi on pakollinen tieto. 5-25 merkkiä."
        elif not description or len(description) < 25:
            error = "Kuvaus on pakollinen tieto. Vähintään 25 merkkiä."
        elif not price or price < 0.01:
            error = "Hinta on pakollinen tieto. Vähintään 0.01 euroa. (Käytä pistettä!)"
        elif not quantity or quantity < 1:
            error = "Määrä on pakollinen tieto. Vähintään 1 kpl."

        image_file = request.files.get('image')

        if not image_file:
            error = "Kuva on pakollinen tieto."
        elif image_file.filename.rsplit(".", 1)[1].lower() not in ["jpg", "jpeg", "png"]:
            error = "Kuvan tulee olla JPG- tai PNG-muodossa."
        else:
            filename = secure_filename(image_file.filename)
            extension = filename.rsplit(".", 1)[1].lower()
            image_type = f"data:image/{extension};base64"

            image = Image.open(image_file)
            image = image.resize((200, 200))

            image_io = BytesIO()
            image.save(image_io, format=extension.upper())
            image_data = image_io.getvalue()

        if error is not None:
            flash(error)
            return redirect(url_for("admin.add"))

        with db.engine.begin() as connection:
            connection.execute(
                text("""
                INSERT INTO Products 
                (user_id, shop_id, name, description, price, quantity, is_available, image_type, image)
                VALUES (:user_id, :shop_id, :name, :description, :price, :quantity, :is_available, :image_type, :image_data)
                """),
                {
                    "user_id": g.user["user_id"],
                    "shop_id": g.user["shop_id"],
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                    "is_available": is_available,
                    "image_type": image_type,
                    "image_data": image_data
                }
            )

        flash("Tuote lisätty.")
        return redirect(url_for("admin.products"))

    return render_template("admin/edit.html",
                           product=[])


@bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    if request.method == "POST":

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

        error = None

        name = request.form.get("name", filtered_product["name"], type=str)
        description = request.form.get(
            "description", filtered_product["description"], type=str)
        price = request.form.get(
            "price", filtered_product["price"], type=float)
        quantity = request.form.get(
            "quantity", filtered_product["quantity"], type=int)
        is_available = bool(request.form.get("is_available"))

        if len(name) < 5 or len(name) > 25:
            error = "Nimi on pakollinen tieto. 5-25 merkkiä."
        elif len(description) < 25:
            error = "Kuvaus on pakollinen tieto. Vähintään 25 merkkiä."
        elif price < 0.01:
            error = "Hinta on pakollinen tieto. Vähintään 0.01 euroa. (Käytä pistettä!)"
        elif quantity < 1:
            error = "Määrä on pakollinen tieto. Vähintään 1 kpl."

        image_file = request.files.get('image')

        if image_file:
            if image_file.filename.rsplit(".", 1)[1].lower() not in ["jpg", "jpeg", "png"]:
                error = "Kuvan tulee olla JPG- tai PNG-muodossa."
            else:
                filename = secure_filename(image_file.filename)
                extension = filename.rsplit(".", 1)[1].lower()
                image_type = f"data:image/{extension};base64"

                image = Image.open(image_file)
                image = image.resize((200, 200))

                image_io = BytesIO()
                image.save(image_io, format=extension.upper())
                image_data = image_io.getvalue()
        else:
            image_type = filtered_product["image_type"]
            image_data = filtered_product["image"]

        if error is not None:
            flash(error)
            return redirect(url_for("admin.edit",
                                    product_id=product_id))

        with db.engine.begin() as connection:
            connection.execute(
                text("""
                UPDATE Products 
                SET name = :name, description = :description, price = :price, quantity = :quantity, is_available = :is_available, image_type = :image_type, image = :image_data
                WHERE product_id = :product_id AND user_id = :user_id
                """),
                {
                    "name": name,
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                    "is_available": is_available,
                    "product_id": product_id,
                    "user_id": g.user["user_id"],
                    "image_type": image_type,
                    "image_data": image_data
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
            "image_src": image_src,
            "is_available": filtered_product["is_available"]
        }

    return render_template("admin/edit.html",
                           product=product_list)


@bp.route("/admin/sales", methods=["GET", "POST"])
@login_required
def sales():
    orders_per_page = 10

    try:
        page = request.args.get(
            "page") or request.form.get("page", 1, type=int)
    except ValueError:
        page = 1

    user_id = g.user["user_id"]

    with db.engine.connect() as connection:
        total_orders = connection.execute(
            text("""
            SELECT COUNT(DISTINCT O.order_id)
            FROM Orders O
            JOIN OrderedProducts OP ON O.order_id = OP.order_id
            JOIN Products P ON OP.product_id = P.product_id
            JOIN Shops S ON P.shop_id = S.shop_id
            WHERE S.user_id = :user_id
            """),
            {"user_id": g.user["user_id"]}
        ).fetchone()[0]

        if total_orders == 0:
            return render_template("admin/sales.html",
                                   orders=[],
                                   current_page=1,
                                   total_pages=1)

        total_pages = (total_orders + orders_per_page - 1) // orders_per_page

        orders = connection.execute(
            text("""
            SELECT O.order_id, O.ordered, P.name, P.description, OP.price AS unit_price, OP.quantity, (OP.price * OP.quantity) AS total_price
            FROM Orders O
            JOIN OrderedProducts OP ON O.order_id = OP.order_id
            JOIN Products P ON OP.product_id = P.product_id
            JOIN Shops S ON P.shop_id = S.shop_id
            WHERE S.user_id = :user_id
            ORDER BY O.ordered DESC
            LIMIT :limit OFFSET :offset
            """),
            {
                "user_id": user_id,
                "limit": orders_per_page,
                "offset": (page-1) * orders_per_page
            }
        ).mappings().fetchall()

    order_list = {}
    for order in orders:
        if order["order_id"] not in order_list:
            order_list[order["order_id"]] = {
                "order_id": order["order_id"],
                "ordered": order["ordered"],
                "products": []
            }
        order_list[order["order_id"]]["products"].append({
            "name": order["name"],
            "description": order["description"],
            "unit_price": order["unit_price"],
            "quantity": order["quantity"],
            "total_price": order["total_price"]
        })

    return render_template("admin/sales.html",
                           orders=order_list.values(),
                           current_page=page,
                           total_pages=total_pages)
