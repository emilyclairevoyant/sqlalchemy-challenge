
"""
This is the Climate Analysis API.
"""

# Import the dependencies.
from sqlalchemy.orm import Session
import numpy as np
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature
    for all the dates greater than or equal to the start date."""
    # Query the minimum, average, and maximum temperatures for dates greater than or equal to the start date
   results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    # Convert the query results to a list of dictionaries
    temperature_data = []
    for min_temp, avg_temp, max_temp in results:
        temperature_data.append({
            'Min Temperature': min_temp,
            'Average Temperature': avg_temp,
            'Max Temperature': max_temp
        })
    session.close()
    # Return the JSON representation of the list
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return a JSON list of the minimum temperature, average temperature, and maximum temperature
    for the dates from the start date to the end date, inclusive."""
    # Query the minimum, average, and maximum temperatures for dates between the start and end dates
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    # Convert the query results to a list of dictionaries
    temperature_data = []
    for min_temp, avg_temp, max_temp in results:
        temperature_data.append({
            'Min Temperature': min_temp,
            'Average Temperature': avg_temp,
            'Max Temperature': max_temp
        })
    session.close()
    # Return the JSON representation of the list
    return jsonify(temperature_data)

