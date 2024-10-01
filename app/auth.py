import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError
from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        error = None

        email = request.form["email"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]

        if not request.form["email"]:
            error = "Sähköpostiosoite on pakollinen tieto."
        elif not firstname or len(firstname) < 2 or len(firstname) > 25:
            error = "Etunimi on pakollinen tieto. 2-25 merkkiä"
        elif not lastname or len(lastname) < 2 or len(lastname) > 25:
            error = "Sukunimi on pakollinen tieto. 2-25 merkkiä."
        elif not password or len(password) < 8 or len(password) > 32:
            error = "Salasana on pakollinen tieto. 8-32 merkkiä."

        try:
            validated_email = validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            error = "Sähköpostiosoite on virheellinen."

        if error is None:
            db = get_db()
            try:
                user_id = db.execute(
                    "INSERT INTO Users (email, firstname, lastname, password) VALUES (?, ?, ?, ?)",
                    (email, firstname, lastname, generate_password_hash(password)),
                ).lastrowid
                db.execute(
                    "INSERT INTO Shops (user_id, name) VALUES (?, ?)",
                    (user_id, f"Käyttäjän {email} verkkokauppa"),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Sähköpostiosoite {email} on jo rekisteröity."
            else:
                flash("Tilin luonti onnistui.")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        error = None

        firstname = request.form["firstname"]
        lastname = request.form["lastname"]

        if not firstname or len(firstname) < 2 or len(firstname) > 25:
            error = "Etunimi on pakollinen tieto. 2-25 merkkiä"
        elif not lastname or len(lastname) < 2 or len(lastname) > 25:
            error = "Sukunimi on pakollinen tieto. 2-25 merkkiä."

        if error is None:
            db = get_db()
            db.execute(
                "UPDATE Users SET firstname = ?, lastname = ? WHERE user_id = ?",
                (firstname, lastname, g.user["user_id"]),
            )
            g.user = get_db().execute(
                "SELECT user_id, firstname, lastname, email, is_admin FROM Users WHERE user_id = ?", (g.user["user_id"],)
            ).fetchone()

            flash("Tietojen päivitys onnistui.")
            return render_template("auth/profile.html")

        flash(error)

    return render_template("auth/profile.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT user_id, password FROM Users WHERE email = ?", (email,)
        ).fetchone()

        if user is None:
            error = "Väärä sähköpostiosoite."
        elif not check_password_hash(user["password"], password):
            error = "Väärä salasana."

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            session["cart"] = {}
            flash("Kirjautuminen onnistui.")
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash('Sinut on kirjattu ulos.')
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT user_id, (SELECT shop_id FROM Shops WHERE user_id=Users.user_id) AS shop_id, firstname, lastname, email, is_admin FROM Users WHERE user_id = ?", (user_id,)
        ).fetchone()
