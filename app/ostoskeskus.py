from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.db import get_db

bp = Blueprint("ostoskeskus", __name__)


@bp.route('/')
def index():
    db = get_db()
    shops = db.execute(
        'SELECT shop_id, user_id, name, description FROM Shops ORDER BY name;'
    ).fetchall()
    return render_template('ostoskeskus/index.html', shops=shops)
