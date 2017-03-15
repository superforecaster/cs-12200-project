This is a README of the files attached with this project:

SUMMARY

The project has the following components:

Project proposal and presentation
Data 
Backend
Frontend

CONTENT

PROJECT PROPOSAL AND PRESENTATION 
- CS122-Project_Super Forecasters.docx:
Project Proposal
-Final-Presentation_2.pptx
Final presentation of the project in the winter quarter 2017
-Super-Forecasters-Pitch2.pptx
First presentation of the project in the winter quarter 2017

DATA:
MINI_DB:
Database composed of 7 tables 
- raw_csv:
Where the csv of the Mexican Ministry of Statistics are located
- process_csv: 
Where the csv after been modified by crime_process.py and csv_process.py. Also contain csv created by dataframe_lasso.py
- Querys
Contains queries to query mini_db
- create_db.sql
Schema to create and upload a sql database with the csv of process_csv (just the csv common with raw_csv).
- db_layout.txt
File with the name of the tables and columns. Each column has the spanish name, english name and name used in the database.
- mini_db
Sql database (.db) created by create_db.sql
-frontend_aux
Auxiliary csv, database and schema for visualization purposes (customized for the frontend API)

BACKEND:




FRONT END

Templates folder: a folder for all the Jinja/html templates for Flask

Static: a javascript file for charts

Flask_frontend_crime.py: A python file with the code to run the website
