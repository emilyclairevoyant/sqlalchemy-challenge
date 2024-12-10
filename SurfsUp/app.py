# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine('sqlite:///SurfsUp/Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON"""
    session = Session(engine)
    
    # Find the most recent date in the data
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    prev_year = most_recent_date - dt.timedelta(days=365)

    # Query precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations as JSON"""
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the last 12 months of temperature observation data (TOBS) for the most active station as JSON"""
    session = Session(engine)

    # Find the most recent date in the data
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    prev_year = most_recent_date - dt.timedelta(days=365)

    # Query the last 12 months of TOBS data for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    session.close()

    # Convert to a list of dictionaries
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return min, avg, and max temperatures from a start date to the end of the dataset"""
    session = Session(engine)

    # Query min, avg, and max temperatures for dates >= start
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    session.close()

    # Return the results as JSON
    if results:
        temp_data = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }
        return jsonify(temp_data)
    else:
        return jsonify({"error": f"No data found for start date {start}"}), 404

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return min, avg, and max temperatures for a specified date range"""
    session = Session(engine)

    # Query min, avg, and max temperatures for dates between start and end
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    # Return the results as JSON
    if results:
        temp_data = {
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        }
        return jsonify(temp_data)
    else:
        return jsonify({"error": f"No data found for the date range {start} to {end}"}), 404

if __name__ == '__main__':
    app.run(debug=True)
