This is a README of the files attached with this project:

BACKEND:

DATA COLLECTION

Data CSVÕs folder: a collection of all the CSVÕs of data i.e. 25 CSVÕs. We used a handful of the CSVÕs for our project i.e. 7 CSVÕs.

Python files:
-csv_cleaning_function.py:
A dynamic function that takes the name of the CSV, cleans the data, organizes the data, and returns a pandas dataframe along with a cleaned CSV of that dataframe.

-crime2_pandas.py
Function that cleans and organizes the data in the crime.csv. The output is a pandas dataframe that sorts


DATA PROCESSING (DATABASES)

-create_db_sql: a schema of the all the CSVÕs/tables (used for predictive stats)
-create_db_crimetype: a single schema/table for the crime file (used for descriptive stats)

DATABASES:
Mini_base.db: a master database (including the crimes)

Crime1.db: a database only of crimes (used for descriptive analytics)


DATA ANALYSIS

Lasso Technique

Lasso_model.py:

Dataframe_lasso.py: 



FRONT END

Templates folder: a folder for all the Jinja/html templates for Flask

Static: a javascript file for charts

Flask_frontend_crime.py: A python file with the code to run the website
