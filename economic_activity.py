import pandas as pd
import csv

years = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008']
with open('economic_activity_by_type.csv', encoding = "ISO-8859-1") as f:
    reader = csv.reader(f)
    #print (type(reader))
    # putting in a large number (5) deliberately
    start_row = 5
    for i, row in enumerate(reader):
        for year in years:
            #print(row, year)
            if year in row:
                #print(row)
                start_row = i
                #print(start_row)

                index_year=row.index(year)
                #print(reader.index(row))
                #print(row[index_year])
                #print(row[index_year:])
                #print(row)


                for year_new in row:
                    if year_new != '':
                        #print(year_new)
                        save_year = year_new
                    elif year_new == '':
                        if row.index(year_new) == 0:
                            row[row.index(year_new)] = 'State Number'
                        elif row.index(year_new) == 1:
                            row[row.index(year_new)] = 'State'
                        else:
                            row[row.index(year_new)] = save_year


                        #print("space", save_year)
                        #print(row.index(year_new))
                        #k = row[index_year:].index(year_new)
                        #print(k)
                        #print(row[index_year:][k], "space")
                        #print(save_year)
                        #row[index_year:][k] = save_year
                        #row[row.index(year_new)] = save_year
                #print(row)

                break
        if i == start_row:
            df = pd.DataFrame(columns=row)
        elif i > start_row + 1:
            df.loc[len(df)] = row
            #print(len(df))
        #print(row)

#print (df)

#df2 = df.unstack()
#df3 = df.unstack()


#df2 = pd.melt(df, id_vars=['State Number', 'State'], var_name="2003", value_name="Value")
#df2 = df2.sort(["State Number", "State"])
#df2 = df.unstack()
#df = df.stack(level=1)
#df.pivot(index='2003', columns='State', values='value')
#pd.pivot_table(df, index=['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011'])
#print (df)



'''
import pandas as pd

econ_df = pd.read_csv('economic_activity_by_type.csv', encoding = "ISO-8859-1")

#print(econ_df.iloc[4:,1:4])

#print(econ_df[[12]])
#econ_df = econ_df.iloc[:,:]
#econ_df = econ_df.loc[:,"2003"]

#a = ['2003']
#k = (econ_df == a).any()

#print(k)

econ_df = econ_df[[1, 2, 7, 12, 17, 22, 27, 32, 37, 42]]
econ_df = econ_df.iloc[4:,:]
econ_df.columns = ['State', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']

#print(econ_df.columns)

#df2 = pd.melt(df, id_vars=["location", "name"], 
#                  var_name="Date", value_name="Value")

print(econ_df)
'''