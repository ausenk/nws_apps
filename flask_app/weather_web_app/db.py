import sqlite3
import click
from flask import current_app, g
from weather_web_app.backend.nws_weather import NwsWeather
from weather_web_app.backend.geo_coder import GeoCoder, ReverseGeoCoder

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    address = "1325 East West Highway Silver Spring, MD 20910"
    coordinates = GeoCoder(address)
    weather_station = NwsWeather(None, coordinates)
    points = weather_station.GetNwsOfficeUsingCoords()
    db.execute(
        'INSERT INTO locations (location_address, latitude, longitude, office, gridx, gridy)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (address, coordinates["lat"], coordinates["long"], points["properties"]["gridId"],\
                points["properties"]["gridX"], points["properties"]["gridY"])
    )
    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialize the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
