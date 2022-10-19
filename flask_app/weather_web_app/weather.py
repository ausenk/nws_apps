from flask import(
    Blueprint, g, session, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from weather_web_app.auth import login_required
from weather_web_app.db import get_db
from weather_web_app.backend.nws_weather import NwsWeather
from weather_web_app.backend.geo_coder import GeoCoder, ReverseGeoCoder

bp = Blueprint("weather", __name__)

@bp.route('/')
def index():
    db = get_db()
    nws_office = db.execute(
        'SELECT MAX(id), location_address, office, gridx, gridy'
        ' FROM locations'
    ).fetchone()

    office = {
        "gridId" : nws_office["office"],
        "gridX" : nws_office["gridx"],
        "gridY" : nws_office["gridy"]
    }
    address = nws_office["location_address"]
    weather_station = NwsWeather(office, None)
    response = weather_station.GetNwsWeather()

    forecast = {
        "address" : address,
        "forecast" : response
    }

    return render_template('weather/index.html')#, forecast=forecast)


@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        locale = request.form['locale']
        error = None

        if not locale:
            error = 'Location is required.'

        coordinates = GeoCoder(locale)
        weather_station = NwsWeather(coordinates)
        points = weather_station.GetNwsOfficeUsingCoords()

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO locations (location_address, latitude, longitude, office, gridx, gridy)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (locale, coordinates["lat"], coordinates["long"], points["properties"]["gridId"],\
                     points["properties"]["gridX"], points["properties"]["gridY"])
            )
            db.commit()

            forecast = {
                "address" : locale,
                "forecast" : points,
                "column_names" :  ["first", "second", "third", "fourth", "fifth"],
                "column_numbers" : [0, 2, 4, 6, 8]
            }

            return render_template('weather/index.html', forecast=forecast)
    
    if request.method == 'PUT':
        locale = request.form['locale']
        error = None

        db = get_db()
        nws_params = db.execute(
            'SELECT office, gridy, gridx'
            ' FROM locations'
            ' WHERE location_address = ?', locale
        ).fetchone()
         
        office = {
            "office" : nws_params["office"],
            "gridx" : nws_params["gridx"],
            "gridy" : nws_params["gridy"]
        }
        weather_station = NwsWeather(office)
        response = weather_station.GetNwsWeather()

        forecast = {
            "address" : locale,
            "forecast" : response,
            "column_names" :  ["first", "second", "third", "fourth", "fifth"],
            "column_numbers" : [0, 2, 4, 6, 8]
        }

        return redirect(url_for('weather.index'), forecast=forecast)


    db = get_db()
    locale = db.execute(
        'SELECT location_address'
        ' FROM locations'
    ).fetchall()

    return render_template('weather/search.html', locale=locale)


@bp.route('/update')
def update():
    pass
