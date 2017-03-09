import sqlite3
import pandas as pd
import numpy as np

################# Auxiliary Functions

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

DATABASE_FILENAME = "mini_base/mini_base"

query = "SELECT * FROM crime c " \
"JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key " \
"JOIN employment e ON c.year = e.year AND c.state_key = e.state_key " \
"JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key " \
"JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key " \
"JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key " \
"JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key"


#Open database
db = sqlite3.connect(DATABASE_FILENAME)
cursor = db.cursor()
r = cursor.execute(query)
results = r.fetchall()
#Obtain headers
header = get_header(cursor)
header = clean_header(header)
#Obtain Pandas DataFrame
df = pd.DataFrame(results)
df.columns = header

#Deleate repeated columns of years, state_keys and state names
df = df.ix[:,~df.columns.duplicated()]
#Replace spanish NaN with NaN
df = df.replace("ND",np.NaN)
df = df.replace("NS", np.NaN)
#Drop columns that don't have complete information
df = df.dropna(axis=1, how='any', thresh=None, subset=None)
#Estimate the lags and the changes (and the lag of the changes)
list_columns = list(df.columns)
df["no_violent"] = pd.to_numeric(df["no_violent"])
del list_columns[0] # del year
del list_columns[0] # del state_key
del list_columns[0] # del state_name
for i in list_columns:
    print(i)
    for j in range(1,4):
        df['{0}L{1}'.format(i,j)] = df.groupby(['state_key'])[i].shift(j)
        if j == 1:
            df["{0}.Ch".format(i)] = (df[i] - df['{0}L1'.format(i)])/(df['{0}L1'.format(i)]+1)
        if j == 2:
            df["{0}.ChL1".format(i)] = (df['{0}L1'.format(i)] - df['{0}L2'.format(i)])/(df['{0}L2'.format(i)]+1)
        if j == 3:
            df["{0}.ChL2".format(i)] = (df['{0}L2'.format(i)] - df['{0}L3'.format(i)])/(df['{0}L3'.format(i)]+1)

#Normalization
list_columns = list(df.columns)
del list_columns[0] # del year
del list_columns[0] # del state_key
del list_columns[0] # del state_name
for i in list_columns:
    df['{0}N'.format(i)] = (df["{0}".format(i)] - df["{0}".format(i)].mean())/df["{0}".format(i)].std()

#Leave just the variables for the prediction
list_columns = list(df.columns)

list_columns_1 = []
for i in list_columns:
    #Variables of year and state 
    if i == "year" or i == "state_key" or i == "state_name":
        list_columns_1.append(i)
    #Dependent variables
    if i == "homicides" or i == "totalN" or i == "violentN" or i == "no_violentN":
        list_columns_1.append(i)
    #if "N" in i and ("L" in i or "ChL" in i):
    if "N" in i and ("L" in i or "ChL" in i):
        list_columns_1.append(i)

#Prepare the database for initial predictions
df_cov = df[df["year"]>=2008]
df_cov = df_cov[list_columns_1]
df_cov = df_cov[df_cov.state_key != 32] #Drop zacatecas because doesn't has complete information

#Close sql connection
db.close()
#Save db local
df.to_csv("mini_base/mini_base.csv", sep='\t')

df_cov.to_csv("mini_base/df_cov.csv", sep='\t')
#Covarinces matrix
covariances = df.corr()
covariances.to_csv("mini_base/covariances.csv", sep='\t')


