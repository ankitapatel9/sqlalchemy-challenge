import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.parser import parse

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

##########################################################    

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

############################################################ 


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


##########################################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # * query for the dates and temperature observations from a year from the last data point.
    
    last_date = session.query(func.max(Measurement.date)).scalar()
    parsed_last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')

    last_year = parsed_last_date - dt.timedelta(days=365)

    temp_data = session.query(Measurement.date,Measurement.tobs).\
            filter(Measurement.date > last_year).\
            order_by(Measurement.date).all()

    session.close()

    # * Return a JSON list of Temperature Observations (tobs) for the previous year.
        
    temperature_observation = []
    for result in temp_data:
        row = {}
        row['date'] = result[0]
        row['tobs'] = result[1]
        temperature_observation.append(row)
    return jsonify(temperature_observation)

##########################################################

@app.route("/api/v1.0/<start>")

def trip_start(start):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d').date()
    return run_start_end_query(start_date, start_date)
    
##########################################################

@app.route("/api/v1.0/<start>/<end>")

def trip_start_and_end(start,end):

    start_date= dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    return run_start_end_query(start_date, end_date)


def run_start_end_query(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # print(f'start : {start_date} , end: {end_date}')
    trip_data = session.query(Measurement.date, func.min(Measurement.tobs),\
                func.avg(Measurement.tobs),\
                 func.max(Measurement.tobs)).\
                filter(Measurement.date.between(start_date, end_date)).\
                group_by(Measurement.date).all()
    session.close()
    records = []
    for result in trip_data:
        row = {}
        row['date'] = result[0]
        row['tmin'] = result[1]
        row['tavg'] = result[2]
        row['tmax'] = result[3]
        records.append(row)
    return jsonify(records)





if __name__ == '__main__':
    app.run(debug=True)
