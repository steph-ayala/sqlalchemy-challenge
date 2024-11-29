from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime
import datetime as dt


app = Flask(__name__)

# Create engine and reflect the tables
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session
session = Session(engine)

# Find the most recent date in the data set (used globally)
recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
recent_date = dt.date.fromisoformat(recent_date_str)
year_ago_date = recent_date - dt.timedelta(days=365)

@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitation data for the last 12 months."""
    # Retrieve precipitation data for the last 12 months
    precip_data = session.query(Measurement.date, func.avg(Measurement.prcp)).\
        filter(Measurement.date >= year_ago_date).\
        group_by(Measurement.date).\
        all()

    # Create a dictionary of the results
    precip_dict = {date: prcp for date, prcp in precip_data}
    
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations."""
    stations = session.query(Station.station).all()
    stations_list = [station[0] for station in stations]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations for the most active station over the last 12 months."""
    # Find the most active station
    most_active_station = session.query(Measurement.station, func.count(Measurement.station).label('observation_count')).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Get temperature data for the most active station for the last 12 months
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= year_ago_date).\
        all()

    # Convert the data into a list of dictionaries
    tobs_list = [{"date": date, "temperature": tobs} for date, tobs in tobs_data]

    return jsonify(tobs_list)

from flask import abort

@app.route("/api/v1.0/<start>")
def start(start):
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        abort(400, description="Invalid date format. Use YYYY-MM-DD.")

# @app.route("/api/v1.0/<start>")
# def start(start):
#     """Return min, avg, max temperatures for dates greater than or equal to the start date."""
#     start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    results = session.query(
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).all()

    temp_stats = results[0]
    return jsonify({
        "TMIN": temp_stats[0],
        "TAVG": temp_stats[1],
        "TMAX": temp_stats[2]
    })

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return min, avg, max temperatures for the date range."""
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    
    results = session.query(
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temp_stats = results[0]
    return jsonify({
        "TMIN": temp_stats[0],
        "TAVG": temp_stats[1],
        "TMAX": temp_stats[2]
    })

if __name__ == "__main__":
    app.run(debug=True)


session.close()

