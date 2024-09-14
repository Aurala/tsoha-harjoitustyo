from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Sähköpostiosoite on pakollinen tieto.'
        elif not firstname:
            error = 'Sähköpostiosoite on pakollinen tieto.'
        elif not lastname:
            error = 'Sähköpostiosoite on pakollinen tieto.'
        elif not password:
            error = 'Sähköpostiosoite on pakollinen tieto.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO Users (email, firstname, lastname, password) VALUES (?, ?, ?, ?)",
                    (email, firstname, lastname, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Sähköpostiosoite {email} on jo rekisteröity."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM Users WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Väärä sähköpostiosoite.'
        elif not check_password_hash(user['password'], password):
            error = 'Väärä salasana.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE user_id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
