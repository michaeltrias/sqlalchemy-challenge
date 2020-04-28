import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)



# Save reference to the table
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
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> "
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
#     # Create our session (link) from Python to the DB
    session = Session(engine)

    previous_year =dt.date(2017,8,23)-dt.timedelta(days=365)

#     """Convert the query results to a dictionary using date as the key and prcp as the value."""
#  
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=previous_year).all()

    session.close()

#    create a dictionary and append to a list
    prcp_data =[]
    for date, prcp in results:
        prcp_dict ={}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
# #     # Create our session (link) from Python to the DB
     session = Session(engine)

# #     """Return a JSON list of stations from the dataset.
# #     
     results = session.query(Measurement.station).group_by(Measurement.station).all()

     session.close()

     return jsonify(results)

# #     # Quer he dates and temperatures observations of the most active station for the last year of data

@app.route("/api/v1.0/tobs")
def tobs():

    previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    session = Session(engine)

    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= previous_year ).all()

    session.close()

    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)
