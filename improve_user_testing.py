import sqlite3
import os
from flask import Flask, render_template, request, redirect
import jinja2

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('templates/')

@app.route('/')
def home():
    return render_template('index.html')
'''
@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    msg = "Login successful. \n The email address is '" + email + "'"
    return render_template('signup.html', msg = msg)
'''

@app.route('/user')
def user_query():
    return render_template('post.html')

@app.route('/year_wise')
def sql_year_wise():

    #year = request.form['value']

    DATA_DIR = os.path.dirname(__file__)
    DATABASE_FILENAME = os.path.join(DATA_DIR, 'crime1.db')

    connection = sqlite3.connect(DATABASE_FILENAME) 
    #connection.row_factory = sql.Row
    cursor_object = connection.cursor()
    # source of following line of code: stackoverflow.com
    cursor_execute = cursor_object.execute("SELECT state_name, primary_activities, secondary_activities from economic_activity where year = 2010 order by primary_activities desc LIMIT 5")
    #cursor_execute = cursor_object.execute("SELECT state_name, total_crime_rate from crime LIMIT where year = ? order by crime_rate")
    rows = cursor_execute.fetchall()
    #print(rows)

    return render_template('list.html', rows = rows)

@app.route('/state_wise')
def sql_state_wise():

    DATA_DIR = os.path.dirname(__file__)
    DATABASE_FILENAME = os.path.join(DATA_DIR, 'crime1.db')

    connection = sqlite3.connect(DATABASE_FILENAME) 

    cursor_object = connection.cursor()
    # source of following line of code: stackoverflow.com
    cursor_execute = cursor_object.execute("SELECT year, total_crime_rate from crime where state = ? order by crime_rate")
    rows = cursor_execute.fetchall()

    return render_template('list.html', rows = rows)

@app.route('/year_state_both')
def sql_year_state_both():

    DATA_DIR = os.path.dirname(__file__)
    DATABASE_FILENAME = os.path.join(DATA_DIR, 'crime1.db')

    connection = sqlite3.connect(DATABASE_FILENAME) 
    cursor_object = connection.cursor()
    cursor_execute = cursor_object.execute("SELECT crime_type, crime_rate from crime where year = ? and state = ? order by crime_rate")
    rows = cursor_execute.fetchall()

    return render_template('list.html', rows = rows)


@app.route('/corr_matrix')
def sql_corr_matrix():

    #year = request.form['value']

    DATA_DIR = os.path.dirname(__file__)
    DATABASE_FILENAME = os.path.join(DATA_DIR, 'crime1.db')

    connection = sqlite3.connect(DATABASE_FILENAME) 
    #connection.row_factory = sql.Row
    cursor_object = connection.cursor()
    # source of following line of code: stackoverflow.com
    cursor_execute = cursor_object.execute("SELECT * from full_database where year = ? and state = ?")
    rows = cursor_execute.fetchall()
    #print(rows)

    return render_template('list.html', rows = rows)


# things to ask
# 1) should I hard code the options in the drop down menu?
# 2) how to link between the SQL querry and the results page?
# 3) 