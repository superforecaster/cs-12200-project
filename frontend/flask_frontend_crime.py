import sqlite3
import os
from flask import Flask, render_template, request, redirect, Markup
import jinja2
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


path = "/home/student/cs-12200-project/frontend/"
path_mini_db = "/home/student/cs-12200-project/Data/mini_db/"
path_crime_db = "/home/student/cs-12200-project/Data/mini_db/frontend_aux/"

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader(path + 'templates/')

#DATA_DIR = os.path.dirname(__file__)


'''DATABASE 1

This database is mini_base which is the master database. This database is used
for predictive analytics and correlation of descriptive analytics.
'''

DATABASE_FILENAME = path_mini_db + 'mini_db'
#DATABASE_FILENAME = os.path.join(DATA_DIR, 'mini_base.db')
connection = sqlite3.connect(DATABASE_FILENAME) 
cursor_object = connection.cursor()


'''DATABASE 2

This database is crime1.db, with only one table i.e. crime rate divided by crime types.
This is used in most of descriptive analytics part.
'''

DATABASE_FILENAME_2 = path_crime_db + 'crime1.db'
#DATABASE_FILENAME_2 = os.path.join(DATA_DIR, 'crime1.db')
connection_2 = sqlite3.connect(DATABASE_FILENAME_2) 
cursor_object_2 = connection_2.cursor()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/descriptive_analysis', methods = ['GET'])
def descriptive_analysis_options():
    '''
    Redirect link:
        after user inputs his desired preference
    '''

    value = request.args['analysis']
    print(value)

    if value == 'descriptive_analysis':
        return render_template('descriptive_analysis.html')
    elif value == 'predictive_analytics':
        return predictive_analytics_options()


@app.route('/descriptive_analysis_decision', methods = ['GET', 'POST'])
def descriptive_analysis_decision():
    '''
    Redirect link:
        after user inputs his desired preference
    '''

    value = request.args['analysis']

    if value == 'state_wise_options':
        return state_wise_options()
    elif value == 'year_wise_options':
        return year_wise_options()
    elif value == 'year_state_both_options':
        return year_state_both_wise_options()
    elif value == 'corr_matrix_options':
        return corr_matrix_decision_options()


'''OPTIONS PAGES'''
'''
Functions under this heading are the drop down options
given to the user. Options are given from the databases directly.
Thus, we are not hardcoding the options given to the user.
'''


@app.route('/year_wise_options')
def year_wise_options():

    sql_querry = "SELECT DISTINCT year from crime;"
    years = sql_options_reader(sql_querry, cursor_object)
    return render_template('post.html', years = years)


@app.route('/state_wise_options')
def state_wise_options():

    sql_querry = "SELECT DISTINCT state_name from crime;"
    states = sql_options_reader(sql_querry, cursor_object)
    return render_template('state_wise_options.html', states=states)


@app.route('/year_state_both_wise_options')
def year_state_both_wise_options():

    sql_querry = "SELECT DISTINCT state_name from crime"
    states = sql_options_reader(sql_querry, cursor_object_2)
    print(states)
    del states[0]

    sql_querry_2 = "SELECT DISTINCT year from crime"
    years = sql_options_reader(sql_querry_2, cursor_object_2)
    del years[0]
    return render_template('year_state_both_wise_options.html', states=states, years=years)


@app.route('/corr_matrix_decision_options', methods = ['GET'])
def corr_matrix_decision_options():
    return render_template('corr_matrix_options.html')


@app.route('/corr_matrix_options', methods = ['GET'])
def corr_matrix_options():

    option = str(request.args['corr_option'])

    if option == 'state_name':

        sql_querry = "SELECT DISTINCT c.state_name FROM crime c \
        JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
        JOIN employment e ON c.year = e.year AND c.state_key = e.state_key \
        JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key \
        JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
        JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key \
        JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key"
        states = sql_options_reader(sql_querry, cursor_object)
        return render_template('corr_matrix_state.html', states=states)

    else:

        sql_querry_2 = "SELECT DISTINCT c.year FROM crime c \
        JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
        JOIN employment e ON c.year = e.year AND c.state_key = e.state_key \
        JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key \
        JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
        JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key \
        JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key"
        
        years = sql_options_reader(sql_querry_2, cursor_object)

        return render_template('corr_matrix_year.html', years=years)


@app.route('/predictive_analytics_options')
def predictive_analytics_options():

    crime_types_list = ['total','violent','homicides','household_crimes','rape','general_homicides',\
    'injuries','other_crimes','kidnap','common_thief','cattle_thief',\
    'banking_thief','highway_thief','no_violent']

    sql_querry = "SELECT DISTINCT year from crime where year >= 2008 and year <= 2011;"

    years = sql_options_reader(sql_querry, cursor_object)

    return render_template('predictive_analytics_options.html', crime_types_list=crime_types_list, years=years)


'''OUTPUT PAGES'''
'''
Functions under this heading are the output from the databases given to the user 
once the user makes the desired selection.
'''

@app.route('/year_wise_output', methods = ['GET'])
def sql_year_wise():

    year = int(request.args['year'])
    header = year

    sql_querry = "SELECT state_name, total from crime where year = ?"
    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year], cursor_object)
    
    column_1_table2 = "Descriptive Statistics"
    column_2_table1 = column_2_table1 + '_crime'

    labels, values, desc_stats, max_value = pandas_desc_stats(rows)

    return render_template('list.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)


@app.route('/state_wise_output', methods = ['GET'])
def sql_state_wise():

    state_name = str(request.args['state_name'])
    header = state_name

    sql_querry = "SELECT year, total from crime where state_name = ?"
    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [state_name], cursor_object)

    column_1_table2 = "Descriptive Statistics"
    column_2_table1 = column_2_table1 + "_crime"
    
    labels, values, desc_stats, max_value = pandas_desc_stats(rows)

    return render_template('list_2.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)


@app.route('/year_state_both_wise_output', methods = ['GET'])
def sql_year_state_both():

    year = int(request.args['year'])
    state_name = str(request.args['state_name'])

    header = state_name
    header2 = year

    sql_querry = "SELECT crime_type, total from crime where year = ? and state_name = ?"
    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year, state_name], cursor_object_2)
    
    column_1_table2 = "Descriptive Statistics"
    column_2_table1 = "crime_rate"

    labels, values, desc_stats, max_value = pandas_desc_stats(rows)

    return render_template('list.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, header2=header2, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)


@app.route('/corr_matrix_output_state', methods = ['GET'])
def sql_corr_matrix_state():

    state_name = str(request.args['state_name'])
    #print(state_name)

    header = state_name

    sql_querry = "SELECT c.year,c.state_key,c.state_name,c.violent,c.no_violent, \
    ca.number_cars,js.suspects_federal_crimes,s.number_strikes, \
    ea.primary_activities,e.employed_pop,e.unemployed_pop, \
    js.rate_sentenced FROM crime c \
    JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
    JOIN employment e ON c.year = e.year AND c.state_key = e.state_key \
    JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key \
    JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
    JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key \
    JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key \
    where c.state_name = ?"

    '''
    sql_querry = "SELECT * FROM crime c \
    JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
    JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
    where c.state_name = ?"
    '''

    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [state_name], cursor_object)
    sql_column_headers = get_header(cursor_object)

    # getting the column names from the header of SQL querry
    num_fields = len(cursor_object.description)
    field_names = [i[0] for i in cursor_object.description]
    field_names = field_names[3:]
    #bro_names = field_names

    k = ",".join(field_names)
    print(k)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    new_df = df.iloc[:,3:]
    new_df.reset_index = field_names
    print(new_df)

    correlation = new_df.corr(method = 'pearson')

    sns.heatmap(correlation, 
        xticklabels=correlation.columns,
        yticklabels=correlation.columns)


    cmap = sns.diverging_palette(5, 250, as_cmap=True)

    v = correlation.style.background_gradient(cmap, axis=1)\
    .set_properties(**{'max-width': '120px', 'font-size': '10pt'})\
    .set_caption(header + " Correlation Matrix " + k)\
    .set_precision(2)\
    .set_table_styles(magnify())

    with open('templates/corr_matrix.html', 'w') as html:
        html.write(v.render())

    return render_template('corr_matrix.html')


@app.route('/corr_matrix_output_year', methods = ['GET'])
def sql_corr_matrix_year():

    year = int(request.args['year'])
    print(year)
    header = year

    sql_querry = "SELECT c.year,c.state_key,c.state_name,c.violent,c.no_violent, \
    ca.number_cars,js.suspects_federal_crimes,s.number_strikes, \
    ea.primary_activities,e.employed_pop,e.unemployed_pop, \
    js.rate_sentenced FROM crime c \
    JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
    JOIN employment e ON c.year = e.year AND c.state_key = e.state_key \
    JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key \
    JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
    JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key \
    JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key \
    where c.year = ?"

    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year], cursor_object)
    
    num_fields = len(cursor_object.description)
    field_names = [i[0] for i in cursor_object.description]
    field_names = field_names[3:]

    k = ",".join(field_names)
    k = "covariates: " + "" + k
    print(k)

    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    new_df = df.iloc[:,3:]
    new_df.reset_index = field_names

    correlation = new_df.corr(method = 'pearson')

    correlation = correlation.fillna(0)

    sns.heatmap(correlation, 
        xticklabels=correlation.columns,
        yticklabels=correlation.columns)

    #sns.plt.show()

    cmap = sns.diverging_palette(5, 250, as_cmap=True)

    v = correlation.style.background_gradient(cmap, axis=1)\
    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})\
    .set_caption(str(header) + " Correlation Matrix" + k) \
    .set_precision(4)\
    .set_table_styles(magnify())

    with open('templates/corr_matrix.html', 'w') as html:
        html.write(v.render())

    return render_template('corr_matrix.html')

@app.route('/predictive_analytics_output', methods = ['GET'])
def sql_predictive_analytics_output():

    import sys
    sys.path.insert(0, '/home/student/cs-12200-project/backend/')
    #import py_file
    import lasso_model

    year = int(request.args['year'])
    crime_type = str(request.args['crime_type'])

    df_actual, df_predicted, df_coeffs, mse, corr = lasso_model.front_end(crime_type, year)

    df_actual1 = df_actual[[2, 3]]

    df_actual_header = list(df_actual1)

    df_predicted = df_predicted.iloc[:, [0, 3]]

    new_df_predicted = pd.concat([df_predicted['state_name'], df_predicted[0]], axis=1)

    new_df_predicted = new_df_predicted.rename(columns = {0: df_actual_header[1]})

    df_coeffs = df_coeffs.rename(columns = {0:'Independent_variables', 1: 'Coefficients'}) 
    df_coeffs1_ascending = df_coeffs.sort('Coefficients', ascending=True)
    df_coeffs1_ascending = df_coeffs1_ascending[:20]

    df_coeffs1_descending = df_coeffs.sort('Coefficients', ascending=False)
    df_coeffs1_descending = df_coeffs1_descending[:20] 

    return render_template("predictive_analytics_output.html", data1=df_actual1.to_html(), data2=new_df_predicted.to_html(), data3=df_coeffs1_ascending.to_html(), data4=df_coeffs1_descending.to_html(), data5=mse)


'''helper functions'''


def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "1em 1em")]),
            dict(selector="th:hover",
                 props=[("font-size", "12pt")]),
            dict(selector="tr:hover td:hover",
                 props=[('max-width', '200px'),
                        ('font-size', '12pt')])
]


def sql_input_reader(sql_querry, argument, cursor_object):

    cursor_execute = cursor_object.execute(sql_querry, argument)    
    rows = cursor_execute.fetchall()

    names = [description[0] for description in cursor_execute.description]

    column_1_table1 = names[0]
    column_2_table1 = names[1]

    return (rows, column_1_table1, column_2_table1)


def sql_options_reader(sql_querry, cursor_object):
    
    cursor_execute = cursor_object.execute(sql_querry)    

    variable = cursor_execute.fetchall()

    return variable


def pandas_desc_stats(rows):
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    df = df.fillna(0)

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    return (labels, values, desc_stats, max_value)

def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break
    return s