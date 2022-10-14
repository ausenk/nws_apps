from flask import(
    Blueprint, g, session, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from weather_web_app.auth import login_required
from weather_web_app.db import get_db
from weather_web_app.backend.weather_getter import WeatherGetter, ParseNwsForcast
from weather_web_app.backend.geo_coder import GeoCoder, ReverseGeoCoder

bp = Blueprint("weather", __name__)

@bp.route('/')
def index():
    db = get_db()
    locale = db.execute(
        'SELECT MAX(id), location_address, office, gridx, gridy'
        ' FROM locations'
        ' LIMIT 1'
    ).fetchone()

    if locale == None or locale["office"] == None:
        coordinates = {
            "lat": 33.9011,
            "long": -117.5179,
        }
        address = ReverseGeoCoder(coordinates)
        weather_station = WeatherGetter(coordinates)
        response = weather_station.GetNwsWeatherUsingCoords()
    else:
        office = {
            "office" : locale["office"],
            "gridx" : locale["gridx"],
            "gridy" : locale["gridy"]
        }
        address = locale["location_address"]
        weather_station = WeatherGetter(office)
        response = weather_station.GetNwsWeatherUsingOffice()
    
    forecast = {
        "address" : address,
        "long_forecast" : ParseNwsForcast(response)
    }

    return render_template('weather/index.html', forecast=forecast)


@bp.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        locale = request.form['locale']
        error = None

        if not locale:
            error = 'Location is required.'

        coordinates = GeoCoder(locale)
        weather_station = WeatherGetter(coordinates)
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
            return redirect(url_for('weather.index'))

    return render_template('weather/search.html')


@bp.route('/update')
def update():
    pass
