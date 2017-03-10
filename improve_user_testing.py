#import StringIO
import sqlite3
import os
from flask import Flask, render_template, request, redirect, Markup
import jinja2
import pandas as pd
import seaborn as sns
import io
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import base64


app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('templates/')

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'mini_base.db')

connection = sqlite3.connect(DATABASE_FILENAME) 
cursor_object = connection.cursor()

'''2'''
DATABASE_FILENAME_2 = os.path.join(DATA_DIR, 'crime1.db')

connection_2 = sqlite3.connect(DATABASE_FILENAME_2) 
cursor_object_2 = connection_2.cursor()



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/descriptive_analysis', methods = ['GET'])
def descriptive_analysis_options():

    value = request.args['analysis']
    print(value)

    if value == 'descriptive_analysis':
        return render_template('descriptive_analysis.html')
    elif value == 'predictive_analytics':
        return predictive_analytics_options()


@app.route('/descriptive_analysis_decision', methods = ['GET', 'POST'])
def descriptive_analysis_decision():

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

    sql_querry = "SELECT DISTINCT state_name from crime;"

    states = sql_options_reader(sql_querry, cursor_object_2)

    sql_querry_2 = "SELECT DISTINCT year from crime;"

    years = sql_options_reader(sql_querry_2, cursor_object_2)

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
        JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key"

        states = sql_options_reader(sql_querry, cursor_object)

        return render_template('corr_matrix_state.html', states=states)

    else:

        sql_querry_2 = "SELECT DISTINCT c.year FROM crime c \
        JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
        JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key"
        
        years = sql_options_reader(sql_querry_2, cursor_object)

        return render_template('corr_matrix_year.html', years=years)



@app.route('/predictive_analytics_options')
def predictive_analytics_options():

    print("BAAA")

    sql_querry = "SELECT DISTINCT state_name from crime;"

    states = sql_options_reader(sql_querry, cursor_object)

    sql_querry_2 = "SELECT DISTINCT year from crime where year >= 2008 and year <= 2011;"

    years = sql_options_reader(sql_querry_2, cursor_object)

    return render_template('predictive_analytics_options.html', states=states, years=years)




'''OUTPUT PAGES'''

@app.route('/year_wise_output', methods = ['GET'])
def sql_year_wise():

    year = int(request.args['year'])

    header = year

    sql_querry = "SELECT state_name, total from crime where year = ? LIMIT 5"
    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year], cursor_object)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    column_1_table2 = "Descriptive Statistics"
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    return render_template('list.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)


@app.route('/state_wise_output', methods = ['GET'])
def sql_state_wise():

    state_name = str(request.args['state_name'])

    header = state_name

    sql_querry = "SELECT year, total from crime where state_name = ? LIMIT 5"
    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [state_name], cursor_object)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    column_1_table2 = "Descriptive Statistics"
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    return render_template('list_2.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)


@app.route('/year_state_both_wise_output', methods = ['GET'])
def sql_year_state_both():

    year = int(request.args['year'])

    state_name = str(request.args['state_name'])

    header = state_name
    header2 = year

    sql_querry = "SELECT crime_type, total from crime where year = ? and state_name = ?"

    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year, state_name], cursor_object_2)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    column_1_table2 = "Descriptive Statistics"
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    return render_template('list.html', rows = rows, labels=labels, values=values, max_value=max_value, header=header, header2=header2, column_1_table1=column_1_table1, column_2_table1=column_2_table1, desc_stats = desc_stats, column_1_table2=column_1_table2)




@app.route('/corr_matrix_output_state', methods = ['GET'])
def sql_corr_matrix_state():

    state_name = str(request.args['state_name'])
    print(state_name)

    header = state_name

    sql_querry = "SELECT * FROM crime c \
    JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
    JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
    where c.state_name = ?"

    #sql_querry = "SELECT crime_type, total from crime where year = ? and state_name = ?"

    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [state_name], cursor_object)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    #print(df.index)

    correlation = df.corr(method = 'pearson')
    print(correlation)

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    column_1_table2 = "Descriptive Statistics"
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    correlation = correlation.fillna(0)

    sns.heatmap(correlation, 
        xticklabels=correlation.columns,
        yticklabels=correlation.columns)

    #sns.plt.show()

    cmap = sns.diverging_palette(5, 250, as_cmap=True)

    v = correlation.style.background_gradient(cmap, axis=1)\
    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})\
    .set_caption(header + " Correlation Matrix")\
    .set_precision(2)\
    .set_table_styles(magnify())

    with open('templates/corr_matrix.html', 'w') as html:
        html.write(v.render())

    return render_template('corr_matrix.html')


@app.route('/corr_matrix_output_year', methods = ['GET'])
def sql_corr_matrix_year():

    print('*****')

    year = int(request.args['year'])
    print(year)
    header = year

    sql_querry = "SELECT * FROM crime c \
    JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key \
    JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key \
    where c.year = ?"

    #sql_querry = "SELECT crime_type, total from crime where year = ? and state_name = ?"

    rows, column_1_table1, column_2_table1 = sql_input_reader(sql_querry, [year], cursor_object)
    
    df = pd.DataFrame( [[ij for ij in i] for i in rows])

    #print(df.index)

    correlation = df.corr(method = 'pearson')
    #print(correlation)

    labels = df[0]
    values = df[1]
    
    # for descriptive statistics
    column_1_table2 = "Descriptive Statistics"
    stats = df.describe()
    desc_stats = []

    for i in range(len(stats.index)):
        stats_tuple = (stats.index[i], stats[1][i])
        desc_stats.append(stats_tuple)

    max_value = max(values)

    correlation = correlation.fillna(0)
    #print(correlation)

    img = BytesIO()

    sns.heatmap(correlation, 
        xticklabels=correlation.columns,
        yticklabels=correlation.columns)

    #sns.plt.show()

    plt.savefig(img, format='png')

    img.seek(0)

    #img.write(plaintext.encode('utf-8'))

    plot_url = base64.b64encode(img.getvalue())

    #print(plot_url)


    cmap = sns.diverging_palette(5, 250, as_cmap=True)

    #print(cmap)

    v = correlation.style.background_gradient(cmap, axis=1)\
    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})\
    .set_caption(str(header) + " Correlation Matrix") \
    .set_precision(2)\
    .set_table_styles(magnify())

    with open('templates/corr_matrix.html', 'w') as html:
        html.write(v.render())

    #'<img src="data:image/png;base64,{}">'.format(plot_url_

    return render_template('corr_matrix.html')

'''
how to make a correlation matrix out of pandas given a year or a state?
just make correlation matrices (pandas styles + sns plot), given a year or a state
'''

'''helper functions'''


def magnify():
    return [dict(selector="th",
                 props=[("font-size", "7pt")]),
            dict(selector="td",
                 props=[('padding', "0em 0em")]),
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


# Things to do
# 1) Styling (separate html for this) (Tuesday)
# 2) heatmaps for year-wise analysis (Wednesday)
# 3) Make a log in page (if time)
# 4) Finish the other three types of graphs (Tuesday)
# 5) make a back hyperlink in each page
# 6) make general functions
# 7) how to separate bar chart from the html and put it into a sep file and then merge?
# 8) how to label axes in bar charts???
# 9) increase the size of the chart a little bit for certain options
# 10) how to display the output in the same page as options page...



# 5) Work on Pedro's ("Predictive Analytics") backend (Wednesday)
