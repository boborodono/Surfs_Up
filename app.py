# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# * Setup Database
# The create_engine() functiion allows us to connect to our database.
engine = create_engine("sqlite:///hawaii.sqlite")

# reflects the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table.
# create a variable for each of the classes to reference later on
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

#* Set up Flask
app = Flask(__name__)

# Define the welcome route (ie. Homepage)
@app.route("/")


# Add routing info for each of the other routes.
def welcome():
    return(
    '''
    Welcome to the Hawaii Climate Analysis API!
    Available Routes:
    /api.v1.0/precipitation
    /api.v1.0/stations
    /api.v1.0/tobs
    /api.v1.0/temp/start/end
    ''')

#//<=================================================================>

# Define the precipitation route
@app.route("/api/v1.0/precipitation")

# add code that calculates the date one year ago from the most recent date in the database
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Write a query to get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp) .\
        filter(Measurement.date >= prev_year).all()
    # Finally, create a dictionary with the date as the key and the precipitation as the value.
    # Jsonify the document
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#//<=================================================================>

# Define the Stations route
@app.route("/api/v1.0/stations")

# add the code that
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#//<=================================================================>

# Define the Monthly Temperature route
@app.route("/api/v1.0/tobs")

# add the code that
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#//<=================================================================>

# Define the Statistics route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

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
