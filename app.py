# Importing Flask
from flask import Flask, jsonify
# Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
import numpy as np

# Conneting to DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Setting up Flask

app = Flask(__name__)

# HTML with links to routes
@app.route("/")
def home():
    print("Loading home page")
    return (
        f"Home page<br/>"
        f"Use links below to load routes<br/><br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/2014-04-01'>2014-04-10</a><br/>"
        f"<a href='/api/v1.0/2014-04-01/2015-04-01'>2014-04-01/2015-04-01</a>"
        )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Loading precipitation page")
    date = '2016-08-23'
    session = Session(engine)
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all() 
    session.close()

    return jsonify(prcp)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Loading stations page")

    session = Session(engine)
    station_list = session.query(Measurement.station).group_by(Measurement.station).all()
    station_list = list(np.ravel(station_list))
    session.close()
    return jsonify(station_list)

# Tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Loading tobs page")
    session = Session(engine)
    tobs_list = session.query(Measurement.tobs).all()
    tobs_list = list(np.ravel(tobs_list))
    session.close()
    return jsonify(tobs_list)

# Start date route

@app.route("/api/v1.0/<start>")
def temps_start(start):
    print("Loading start date page")
    session = Session(engine)
    x = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    return jsonify(x)

# Start/End dates route

@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    print("Loading start/end dates page")
    session = Session(engine)
    y=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(y)

if __name__ == "__main__":
    app.run(debug=True)