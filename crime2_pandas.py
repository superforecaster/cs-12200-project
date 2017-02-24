import pandas as pd

crime_df = pd.read_csv('crime2.csv', encoding = "ISO-8859-1")


# converting the numbers from object to ints
crime_df.iloc[:,5:18] = crime_df.iloc[:,5:18].apply(pd.to_numeric, errors = 'coerce')


# adding the Total column
crime_df["Total"] = crime_df['January'] + crime_df['February'] + crime_df['March'] + crime_df['April'] + crime_df['May'] + crime_df['June'] + crime_df['July'] + crime_df['August'] + crime_df['September'] + crime_df['October'] + crime_df['November'] + crime_df['December']

#+ crime_df[[january+2]] + crime_df[[january+3]]
#+ crime_df[[january+4]] + crime_df[[january+5]] + crime_df[[january+6]] + crime_df[[january+7]] + crime_df[[january+8]]
#+ crime_df[[january+9]] + crime_df[[january+10]] + crime_df[[january+11]]

crime_df.drop(crime_df.columns[4:18], axis=1, inplace=True)
crime_df.columns = ['Year', 'State', 'State_ID', 'Crime_type', 'Total']


crime_df = crime_df.groupby(by=['Year', 'State', 'State_ID', 'Crime_type'])['Total'].sum().to_frame().reset_index()


crime_df.set_index(['Year', 'State', 'State_ID'], append=False, inplace=True)


#print(crime_df)
crime_df.pivot(index='Year', values='Total', columns='Crime_type')

print(crime_df)

# Sort by Time-Series
#crime_df_groupby_1 = crime_df.groupby(by=['Year', 'ENTIDAD'])['Total'].sum().to_frame()
#print(crime_df_groupby_1)