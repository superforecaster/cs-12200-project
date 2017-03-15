import pandas as pd
import csv

path = "/home/student/cs-12200-project/Data/mini_db/"

years = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011']

#Put here the tables that you want to convert
table_name = ["economic_activity_by_type.csv","strikes.csv","employment.csv","urbanization.csv","justice_system.csv","cars.csv"] 

def data_cleaning_inter(file_name):
    """
    This function takes the filenames of a csv, and cleans it. 

    Returns:
        The function returns the multi-index column parameters of a csv file.
    """

    file_name = path + 'raw_csv/{0}'.format(file_name)
    years_filtered = []
    indices_second_row = []
    second_column_list = []

    with open(file_name, encoding = "ISO-8859-1") as f:
        reader = csv.reader((line.replace('\0','') for line in f), delimiter=",")
        start_row = 5
        for i, row in enumerate(reader):
            if i >0 and i < 5:
                for year in years:
                    if year in row:
                        start_row = i

                        index_year = row.index(year)

                        for year_new in row:
                            if year_new != '':
                                years_filtered.append(year_new)
                                indices_second_row.append(row.index(year_new))                           
                        break

            if i > start_row + 1:
                if i == start_row + 2:
                    first_position = indices_second_row[0]
                    while first_position < indices_second_row[1]:
                        second_column_list.append(row[first_position])
                        first_position += 1

    return years_filtered, second_column_list, start_row, file_name


def data_cleaning_final(years_filtered, second_column_list, start_row,file_name):
    """
    This function takes the multi-index parameters and sorts the dataframes.

    Returns:
        Cleaned multi-index dataframes sorted by year, state_name and state_key
    """

    years_filtered = years_filtered
    second_column_list = second_column_list
    start_row = start_row
    
    df = pd.read_csv(path +"raw_csv/{0}".format(file_name), encoding = "ISO-8859-1", header = start_row + 2, index_col = "Nombre")

    df.index.rename('State', inplace = True)

    df.set_index("Clave", append=True, inplace=True)

    mux = pd.MultiIndex.from_product([years_filtered, second_column_list])

    df.columns = mux
    
    df = df.stack(0)

    df = df.swaplevel(0,1)

    df = df.sortlevel(2)

    df.index.names = ['State_ID', 'State', 'Year']

    df = df.reorder_levels(['Year', 'State_ID', 'State']) #, columns=['Year', 'State ID', 'State'])

    df.to_csv(path_or_buf = path + "process_csv/{0}".format(file_name), sep = ',')


# automatically generating all the cleaned CSV's

for i in table_name:
    years_filtered, second_column_list, start_row, file_name = data_cleaning_inter(i)
    data_cleaning_final(years_filtered, second_column_list, start_row, i)
