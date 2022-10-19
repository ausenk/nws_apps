import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from weather_web_app.db import get_db
from .validate import validate_user_data
from weather_web_app.backend.nws_weather import NwsWeather
from weather_web_app.backend.geo_coder import GeoCoder, ReverseGeoCoder

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # User submits information to be posted to the database
    if request.method == 'POST':
        user_info = {
            'username' : request.form['username'],
            'password' : request.form['password'],
            'email' : request.form['email'],
            'phone' : request.form['phone'],
            'addr' : request.form['addr'],
        }
        db = get_db()
        error = None
        # Validate the input data
        error = validate_user_data(**user_info)

        coordinates = GeoCoder(user_info["addr"])
        weather_station = WeatherGetter(coordinates)
        points = weather_station.GetNwsOfficeUsingCoords()

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email, phone, user_addr, \
                        user_latitude, user_longitude, user_office, user_gridx, user_gridy)\
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_info['username'], generate_password_hash(user_info['password']),\
                        user_info['email'], user_info['phone'], user_info['addr'],\
                            coordinates["lat"], coordinates["long"], points["properties"]["gridId"], \
                                points["properties"]["gridX"], points["properties"]["gridY"])
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {user_info['username']} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['addr'] = user['user_addr']
            session['phone'] = user['phone']
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
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
        