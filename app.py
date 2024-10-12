# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Initialize the Flask app
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Home route
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months"""
    # Find the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary using 'date' as the key and 'prcp' as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all stations
    stations_data = session.query(Station.station).all()

    # Convert the query result into a list
    stations_list = list(np.ravel(stations_data))

    return jsonify(stations_list)

# TOBS (temperature observations) route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station over the last year"""
    # Find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the most recent date
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the temperature observations for the last year for the most active station
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query result into a list
    temperature_list = list(np.ravel(temperature_data))

    return jsonify(temperature_list)

# Temperature range route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return the min, avg, and max temperature for all dates greater than or equal to the start date, 
    or for a range between the start and end date"""
    

    # Query the temperature statistics (TMIN, TAVG, TMAX)
    if end:
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    # Convert the query result into a dictionary
    temperature_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    return jsonify(temperature_dict)

# Close the session when shutting down the app
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()

if __name__ == '__main__':
    app.run(debug=True)