from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError
from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":

        error = None

        email = request.form["email"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]

        if not request.form["email"]:
            error = "Sähköpostiosoite on pakollinen tieto."
        elif not firstname or len(firstname) < 2:
            error = "Etunimi on pakollinen tieto. Vähintään 2 merkkiä"
        elif not lastname or len(lastname) < 2:
            error = "Sukunimi on pakollinen tieto. Vähintään 2 merkkiä."
        elif not password or len(password) < 6:
            error = "Salasana on pakollinen tieto. Vähintään 6 merkkiä."

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
                    "INSERT INTO Shops (user_id, name, description) VALUES (?, ?, ?)",
                    (user_id, f"Käyttäjän {email} verkkokauppa", f"Verkkokaupan kuvaus"),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Sähköpostiosoite {email} on jo rekisteröity."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/profile", methods=("GET", "POST"))
def edit():
    return render_template("auth/profile.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM Users WHERE email = ?", (email,)
        ).fetchone()

        if user is None:
            error = "Väärä sähköpostiosoite."
        elif not check_password_hash(user["password"], password):
            error = "Väärä salasana."

        if error is None:
            session.clear()
            session["user_id"] = user["user_id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM Users WHERE user_id = ?", (user_id,)
        ).fetchone()
