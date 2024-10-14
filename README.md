# sqlalchemy-challenge

The objective of this homework is to analyze climate data for Hawaii, and create a Flask API to display the results of the analysis. The data comes from a SQLite database that contains information on precipitation, temperature observations, and weather stations in Hawaii.

Part 1: Data Analysis
# Import dependencies
Reflect Tables in to SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
# create engine to hawaii.sqlite
# reflect an existing database into a new model
# reflect the tables
# View all of the classes that automap found
# Save references to each table
# Create our session (link) from Python to the DB
Exploratory Precipitation Analyses
# Find the most recent date in the data set.
# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
# Calculate the date one year from the last date in data set.
# Perform a query to retrieve the data and precipitation scores
# Save the query results as a Pandas DataFrame. Explicitly set the column names
# Sort the dataframe by date
# Use Pandas Plotting with Matplotlib to plot the data
# Use Pandas to calculate the summary statistics for the precipitation data
Exploratory Station Analysis
# Design a query to calculate the total number of stations in the dataset
# Design a query to find the most active stations (i.e. which stations have the most rows?)
# List the stations and their counts in descending order.
# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
# Convert the query result into a DataFrame
# Plot the results as a histogram
Close Session
# Close Session

Part 2: Flask API Development
Built a Flask web application that serves the results of the analysis through multiple API routes
# Import the dependencies
# DATABASE SETUP
# Create engine using the 'hawaii.sqlite'
# Declare a Base using 'automap_base()'
# Use the Base class to reflect the database tables
# Assign the measurement class to a variable called 'Measurement' and the station class to a variable called 'station'
# Flask Setup
# Initialize the Flask app
# FLASK SETUP
# Initialize the Flask app
# FLASK ROUTES
# Home Routes (/): displays all the available API routes.
# Precipitation route (/api/v1.0/precipitation):returns precipitation data for the last 12 months in JSON format.
  # Find the most recent date in the dataset
  # Query for the last 12 months of precipitation data
  # Create a dictionary using 'date' as the key and 'prcp' as the value
# Stations route (/api/v1.0/stations): returns a list of weather stations across Hawaii.
  # Query all stations
  # Convert the query result into a list
# TOBS (temperature observations) route (/api/v1.0/tobs): returns temperature observations for the most active station over the last 12 months.
  # Find the most active station
  # Calculate the date one year ago from the most recent date
  # Query the temperature observations for the last year for the most active station
  # Convert the query result into a list
# Temperature range route 
  # Filter for data after the start date (/api/v1.0/<start>): returns the minimum, average, and maximum temperature from a given start date.
  # Filter between start and end date (/api/v1.0/<start>/<end>: returns the minimum, average, and maximum temperature for the date range specified by the start and end dates.
  # Convert the query result into a dictionary
