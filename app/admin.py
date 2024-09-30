from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

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
            db = get_db()
            try:
                db.execute(
                    "UPDATE Shops SET name = ?, description = ?, is_available = 1 WHERE user_id = ?",
                    (name, description, g.user["user_id"]),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Kauppa nimeltä {name} on jo olemassa."
            else:
                flash("Kauppasi on nyt aktivoitu.")
                return redirect(url_for("admin.shop"))

        flash(error)

    db = get_db()

    shop = db.execute(
        "SELECT shop_id, user_id, name, description, is_available FROM shops WHERE user_id = ?",
        (g.user["user_id"],)
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

    db = get_db()

    total_products = db.execute("SELECT COUNT(product_id) FROM Products WHERE user_id = ?;",
                                (g.user["user_id"],)
                                ).fetchone()
    
    if total_products[0] == 0:
        flash("Sinulla ei ole tuotteita")
        render_template("admin/products.html", products=[], current_page=1, total_pages=1)

    total_pages = (total_products[0] + products_per_page - 1) // products_per_page

    filtered_products = db.execute("SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE user_id = ? ORDER BY product_id DESC LIMIT ? OFFSET ?;",
                                   (g.user["user_id"], products_per_page, (page-1)*products_per_page)
                                   ).fetchall()
    
    return render_template("admin/products.html", products=filtered_products, total_products=total_products[0], current_page=page, total_pages=total_pages)


@bp.route("/edit", methods=["GET"])
@login_required
def edit():
    return render_template("admin/edit.html")


@bp.route("/sales", methods=["GET"])
@login_required
def sales():
    return render_template("admin/sales.html")
