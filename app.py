import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station



# Flask Setup
#################################################
app = Flask(__name__)

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

@app.route("/api/v1.0/precipitation")
def percipitation():


    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    rain_totals = []
    for result in results:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

    # Return the JSON representation of your dictionary.
@app.route("/api/v1.0/stations")

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations_query = session.query(Station.name, Station.station)
    session.close()
    station_data = []
    for result in stations_query:
        row = {}
        row["name"] = result[0]
        row["station"] = result[1]
        station_data.append(row)

    return jsonify(station_data)


if __name__ == '__main__':
    app.run(debug=True)
