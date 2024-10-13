# Import the dependencies.
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

#################################################
# Database Setup
#################################################

# Create engine using the 'hawaii.sqlite'
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using 'automap_base()'
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called 'Measurement' and the station class to a variable called 'station'
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available API routes"""
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
    session = Session(engine)

    # Find the most recent date in the dataset
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query for the last 12 months of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Create a dictionary using 'date' as the key and 'prcp' as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    session = Session(engine)

    # Query all stations
    stations_data = session.query(Station.station).all()

    session.close()

    # Convert the query result into a list
    stations_list = list(map(lambda x: x[0], stations_data))

    return jsonify(stations_list)

# TOBS (temperature observations) route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the most active station over the last year"""
    session = Session(engine)

    # Find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Calculate the date one year ago from the most recent date
    latest_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(latest_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the temperature observations for the last year for the most active station
    temperature_data = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Convert the query result into a list
    temperature_list = list(map(lambda x: x[0], temperature_data))

    return jsonify(temperature_list)

# Temperature range route
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    """Return the min, avg, and max temperature for all dates greater than or equal to the start date, 
    or for a range between the start and end date"""
    session = Session(engine)

    if end:
        # Filter between start and end date
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        # Filter for data after the start date
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    session.close()

    # Convert the query result into a dictionary
    temperature_dict = {
        "TMIN": temperature_stats[0][0],
        "TAVG": temperature_stats[0][1],
        "TMAX": temperature_stats[0][2]
    }

    return jsonify(temperature_dict)

if __name__ == '__main__':
    app.run(debug=True)