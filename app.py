# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables 
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23_2017-01-01"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation for last 12 months"""
    
    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query measurement table for date, prcp
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of yearly_precipitation
    yearly_precipitation = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        yearly_precipitation.append(precipitation_dict)

    return jsonify(yearly_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query station table for station data
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for id, name, station, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the temperatures for the most active station for last 12 months"""
    
    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query measurement table for date, tobs
    
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of active_yearly_temps
    active_yearly_temps = []
    for date,tobs in results:
        active_temp_dict = {}
        active_temp_dict["date"] = date
        active_temp_dict["tobs"] = tobs
        active_yearly_temps.append(active_temp_dict)

    return jsonify(active_yearly_temps)

@app.route("/api/v1.0/2016-08-23")
def startdate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max, average values for all dates greater than or equal to the specified start date of 2016-08-23"""
    
    # Set the query date.
    query_date = dt.date(2016, 8, 23)
    # assign variables for min, max, avg temps in the date range
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)
    
    # assign variables for min, max, avg temps in the date range
    results = session.query(temp_min, temp_max, temp_avg).filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of startdate_temps
    startdate_temps = []
    for temp_min,temp_max, temp_avg in results:
        startdate_dict = {}
        startdate_dict["min_temp"] = temp_min
        startdate_dict["max_temp"] = temp_max
        startdate_dict["avg_temp"] = temp_avg
        startdate_temps.append(startdate_dict)

    return jsonify(startdate_temps)

@app.route("/api/v1.0/2016-08-23_2017-01-01")
def start_end_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max, average values for all dates between 2016-08-23 and 2017-01-01 inclusive"""
    
    # Set the query date.
    start_date = dt.date(2016, 8, 23)
    end_date = dt.date(2017,1,1)

    # assign variables for min, max, avg temps in the date range
    temp_min = func.min(Measurement.tobs)
    temp_max = func.max(Measurement.tobs)
    temp_avg = func.avg(Measurement.tobs)

    #Query for min, max, avg temps for dates between 2016-08-23 and 2017-01-01 inclusive
    results = session.query(temp_min, temp_max, temp_avg).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_end_date_temps
    start_end_date_temps = []
    for temp_min,temp_max, temp_avg in results:
        startenddate_dict = {}
        startenddate_dict["min_temp"] = temp_min
        startenddate_dict["max_temp"] = temp_max
        startenddate_dict["avg_temp"] = temp_avg
        start_end_date_temps.append(startenddate_dict)

    return jsonify(start_end_date_temps)

if __name__ == '__main__':
    app.run(debug=True)