
# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Finally, add the code to import the dependencies that we need for Flask. 
# You'll import these right after your SQLAlchemy dependencies.
from flask import Flask, jsonify

# In order to connect to our SQLite database, we need to use the create_engine() function.
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model with the automap_base() function.
Base = automap_base()

# reflect the tables with the prepare() function.
Base.prepare(engine, reflect=True)

# save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# we need to define our app for our Flask application.
# Notice the __name__ variable in this code. 
# This is a special type of variable in Python. Its value depends on where and how the code is run.
app = Flask(__name__)

# Create the Welcome Route
@app.route("/")

# First, create a function welcome() with a return statement. 
# El elemento HTML line break <br> produce un salto de línea en el texto (retorno de carro)
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end<br>
    ''')

# Every time you create a new route, your code should be aligned to the left in order to avoid errors
@app.route("/api/v1.0/precipitation")

# We'll create a dictionary with the date as the key and the precipitation as the value. 
# To do this, we will "jsonify" our dictionary. Jsonify() is a function that converts the dictionary to a JSON file.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
     filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Stations Route
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Monthly Temperature Route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # Unravel the results into a one-dimensional array and convert that array into a list.   
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Statistics Route
# This route is different from the previous ones in that we will have to provide both a starting and ending date    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# With the function declared, we can now create a query to select the minimum, average, and maximum temperatures from our SQLite database.
# We'll start by just creating a list called sel
# Since we need to determine the starting and ending date, add an if-not statement to our code. 
# This will help us accomplish a few things. We'll need to query our database using the list that we just made. 
# Then, we'll unravel the results into a one-dimensional array and convert them to a list. 
# Finally, we will jsonify our results and return them.

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

# For debug errors:
# Enable debug mode so Flask will actually tell you what the error is.
# Taken from: https://stackoverflow.com/questions/10219486/flask-post-request-is-causing-server-to-crash
if __name__ == '__main__':
    app.debug = True
    app.run()







