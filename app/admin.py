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
    if request.method == "POST":
        pass
    
    db = get_db()
    own_products = db.execute(
        "SELECT product_id, (SELECT name FROM Shops WHERE Shops.shop_id=Products.shop_id) AS shop_name, name, description, image, price, quantity FROM Products WHERE user_id=? ORDER BY product_id DESC;",
        (g.user["user_id"],)
    ).fetchall()

    return render_template("admin/products.html", products=own_products)


@bp.route("/sales", methods=("GET", "POST"))
@login_required
def sales():
    return render_template("admin/sales.html")
