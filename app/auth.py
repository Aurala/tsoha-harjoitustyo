import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app.db import db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

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
        streetaddress = request.form["streetaddress"]
        postalcode = request.form["postalcode"]
        city = request.form["city"]

        if not request.form["email"]:
            error = "Sähköpostiosoite on pakollinen tieto."
        elif not firstname or len(firstname) < 2 or len(firstname) > 25:
            error = "Etunimi on pakollinen tieto. 2-25 merkkiä"
        elif not lastname or len(lastname) < 2 or len(lastname) > 25:
            error = "Sukunimi on pakollinen tieto. 2-25 merkkiä."
        elif not streetaddress or len(streetaddress) < 5 or len(streetaddress) > 25:
            error = "Katuosoite on pakollinen tieto. 5-25 merkkiä."
        elif not postalcode or len(postalcode) != 5:
            error = "Postinumero on pakollinen tieto. 5 merkkiä."
        elif not city or len(city) < 2 or len(city) > 25:
            error = "Kaupunki on pakollinen tieto. 2-25 merkkiä."
        elif not password or len(password) < 8 or len(password) > 32:
            error = "Salasana on pakollinen tieto. 8-32 merkkiä."

        try:
            validated_email = validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            error = "Sähköpostiosoite on virheellinen."

        if error is None:
            try:
                with db.engine.begin() as connection:
                    result = connection.execute(
                        text("""
                        INSERT INTO Users (email, firstname, lastname, streetaddress, postalcode, city, password)
                        VALUES (:email, :firstname, :lastname, :streetaddress, :postalcode, :city, :password)
                        RETURNING user_id
                        """),
                        {
                            "email": email,
                            "firstname": firstname,
                            "lastname": lastname,
                            "streetaddress": streetaddress,
                            "postalcode": postalcode,
                            "city": city,
                            "password": generate_password_hash(password)
                        }
                    ).mappings().fetchone()
                    user_id = result.fetchone("user_id")
                    connection.execute(
                        text("""
                        INSERT INTO Shops (user_id, name) VALUES (:user_id, :shop_name)
                        """),
                        {
                            "user_id": user_id,
                            "shop_name": f"Käyttäjän {email} verkkokauppa"
                        }
                    )
            except IntegrityError:
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
        streetaddress = request.form["streetaddress"]
        postalcode = request.form["postalcode"]
        city = request.form["city"]

        if not firstname or len(firstname) < 2 or len(firstname) > 25:
            error = "Etunimi on pakollinen tieto. 2-25 merkkiä."
        elif not lastname or len(lastname) < 2 or len(lastname) > 25:
            error = "Sukunimi on pakollinen tieto. 2-25 merkkiä."
        elif not streetaddress or len(streetaddress) < 5 or len(streetaddress) > 25:
            error = "Katuosoite on pakollinen tieto. 5-25 merkkiä."
        elif not postalcode or len(postalcode) != 5:
            error = "Postinumero on pakollinen tieto. 5 merkkiä."
        elif not city or len(city) < 2 or len(city) > 25:
            error = "Kaupunki on pakollinen tieto. 2-25 merkkiä."

        if error is None:
            try:
                with db.engine.begin() as connection:
                    connection.execute(
                        text("""
                        UPDATE Users SET firstname = :firstname, lastname = :lastname, streetaddress = :streetaddress, postalcode = :postalcode, city = :city 
                        WHERE user_id = :user_id
                        """),
                        {
                            "firstname": firstname,
                            "lastname": lastname,
                            "streetaddress": streetaddress,
                            "postalcode": postalcode,
                            "city": city,
                            "user_id": g.user["user_id"]
                        }
                    )
                    g.user = connection.execute(
                        text("""
                        SELECT user_id, firstname, lastname, streetaddress, postalcode, city, email, is_admin
                        FROM Users
                        WHERE user_id = :user_id
                        """),
                        {
                            "user_id": g.user["user_id"]
                        }
                    ).fetchone()

                flash("Tietojen päivitys onnistui.")
                return render_template("auth/profile.html")

            except IntegrityError as e:
                db.session.rollback()
                error = "Virhe päivitettäessä käyttäjän tietoja."

        flash(error)

    return render_template("auth/profile.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        with db.engine.connect() as connection:
            user = connection.execute(
                text("""
                SELECT user_id, password
                FROM Users
                WHERE email = :email
                """),
                {
                    "email": email
                }
            ).mappings().fetchone()

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
        with db.engine.connect() as connection:
            g.user = connection.execute(
                text("""
                SELECT U.user_id, U.firstname, U.lastname, U.streetaddress, U.postalcode, U.city, U.email, U.is_admin, S.shop_id
                FROM Users U
                LEFT JOIN Shops S ON U.user_id = S.user_id
                WHERE U.user_id = :user_id
                """),
                {
                    "user_id": user_id
                }
            ).mappings().fetchone()
