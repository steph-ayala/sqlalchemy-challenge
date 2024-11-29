# sqlalchemy-challenge

This project provides a Flask-based API for exploring and analyzing climate data for Honolulu, Hawaii. The API interacts with a SQLite database (hawaii.sqlite) and allows users to query precipitation and temperature data through several endpoints.

Key Features
Flask API: Exposes several routes to retrieve climate data.
SQLAlchemy: Interacts with the SQLite database to fetch climate data.
Routes:
/api/v1.0/precipitation: Returns precipitation data for the last 12 months.
/api/v1.0/stations: Lists all stations in the dataset.
/api/v1.0/tobs: Provides temperature observations for the most active station.
/api/v1.0/<start>: Returns temperature stats (min, avg, max) from a specified start date.
/api/v1.0/<start>/<end>: Returns temperature stats for a date range.

Example Routes
Precipitation Data:

Copy code
curl http://127.0.0.1:5000/api/v1.0/precipitation
Station List:

Copy code
curl http://127.0.0.1:5000/api/v1.0/stations
Temperature Observations:

Copy code
curl http://127.0.0.1:5000/api/v1.0/tobs
Temperature Stats from Start Date:

Copy code
curl http://127.0.0.1:5000/api/v1.0/2016-08-23

Resources:
Tutoring
XPert 
Youtube
chatGPT
Class Activites
