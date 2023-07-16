# Import the dependencies.

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify 

import numpy as np

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:////Users/brennancurrie/Desktop/My_Code/My_Repos/sqlalchemy-challenge/Resources/hawaii.sqlite?check_same_thread=False")
# ?check_same_thread=False   So, the error basically means the instance of the db engine is trying to work on multiple threads, which by default, SQLite doesn't allow. So, what we want to do is tell it, it's okay to do so!

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

##Create App
app = Flask(__name__)

#################################################
# Flask Static Routes
#################################################

#HOME ROUTE
@app.route("/")
def home():
    return """WELCOME TO THE HOME PAGE! ___
            
            Available Routes:
            
            /precipitation for precipitation data,
            /stations for station data,
            /tobs for temperature data,
            /start/(input start date), 
            /customdaterange/(input start date)/(input end date)"""

#PRECIPITATION ROUTE
@app.route("/precipitation")
def precipitation():
    results =   session.query(measurement.date, measurement.prcp).filter(measurement.station == 'USC00519281').\
                order_by(measurement.date.desc()).limit(365)

    precipdict = [{'Date': result[0], 'Precipitation' : result[1]} for result in results]
    return jsonify(precipdict)

#STATION ROUTE
@app.route("/stations")
def stations():
    stationlist = session.query(station.station).all()
    #stations = list(np.ravel(stationlist))
    stationlist
    emptyliststation = []
    for row in stationlist:
        emptyliststation.append(row[0])
    return jsonify(emptyliststation)

#TOBS ROUTE
@app.route("/tobs")
def tobs():
    results2 =  session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                order_by(measurement.date.desc()).limit(365)

    tobsdict = [{'Date': result[0], 'Temperature' : result[1]} for result in results2]
    return jsonify(tobsdict)

#################################################
# Flask Dynamic Routes
#################################################

@app.route("/temp/<start>")
def start(start=None):
    startquery = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
            filter(measurement.station == 'USC00519281').filter(measurement.date >= start).limit(365)
    startdict = [{'Min': result[0], 'Max' : result[1], 'Avg' : round(result[2],0)} for result in startquery]
                 
    print(startdict)
    return jsonify(startdict)


@app.route('/customdaterange/<start>/<end>')
def startend(start=None, end=None):

    startendquery = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                    filter(measurement.station == 'USC00519281').\
                    filter(measurement.date >= start).\
                    filter(measurement.date <= end).all()
    
    startenddict = [{'Min': result[0], 'Max' : result[1], 'Avg' : round(result[2],0)} for result in startendquery]

    print(start,end)
    return jsonify(startenddict)


if __name__== "__main__": 
    app.run(debug=True)



################################################
#PROJECT NOTES
#Here's what each line of the code does:
#1. @app.route("/stations"): This is a decorator that specifies the URL path that will trigger the stations function. In this case, the URL path is /stations.
#2. def stations():: This defines the stations function. It takes no arguments.
#3. results = session.query(Station.station).all(): This line of code queries a database to retrieve a list of station names from a table called Station. It uses SQLAlchemy's query method to specify that we only want the station column, and then the all method to retrieve all of the rows in the table.
#4. session.close(): This line of code closes the database session to free up resources.
#5. stations = list(np.ravel(results)): This line of code takes the list of tuples returned by the query method and converts it into a flat list of station names.
#6. return jsonify(stations=stations): This line of code converts the stations list into a JSON response that can be returned to the client making the API request.

##if __name__ == "__main__": checks to see if this module was called interactively and then calls the specified function to execute the code. 
# So app. run would only execute if this module was call interactively and would not execute if this module was imported into another module.