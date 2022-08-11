# Set Up the Flask Weather App:
import datetime as dt
import numpy as np
import pandas as pd

# SQLAlchemy dependencies:
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#  Import the dependencies for Flask:
from flask import Flask, jsonify

###

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes.
Base = automap_base()

# Reflect the database:
Base.prepare(engine, reflect=True)

# Save references to each table:
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

###

# Set up Flask:
app = Flask(__name__)

# Create the Welcome Route

#Define the welcome route
@app.route("/")

# Create a function for routing information:

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')  # When creating routes, we follow the naming convention /api/v1.0/
          #followed by the name of the route   


# Build the Precipitation Route

# Create the route:
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function
def precipitation():
    # Query to get the date and precipitation for the previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key./
    # and the precipitation as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Build the Stations Route:

# Create the route:
@app.route("/api/v1.0/stations")

# Create the stations() function
def stations():
    # Query to get all of the stations in our database
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Build Monthly Temperature Route:

# Create the route:
@app.route("/api/v1.0/tobs")

# Create the temp_monthly() function:
def temp_monthly():
    # Get the date one year ago from the last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the primary station for the temp observations from the prior year
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # Unravel the results into a one-dimensional array & Convert array into a list
    temps = list(np.ravel(results))
    # jsonify our temps list:
    return jsonify(temps=temps)

# Statistics Route - Report Min,Avg & Max temps:
# Create the route, for start and ending date:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a function stats():

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# After running the flask run, we got a [null,null,null] answer
# On the web browser fix the date to include a start/end date
