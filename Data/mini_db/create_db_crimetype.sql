CREATE TABLE crime
   (year integer,
   state_name varchar(50),
   state_key integer,
   crime_type varchar(50),
   total integer);

.separator ","
.import crime_df_crimetype.csv crime
