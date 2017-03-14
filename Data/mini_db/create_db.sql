
-- DEPENDENT VARIABLE (CRIME)
-- COVARIATES
CREATE TABLE crime
   (year integer,
   state_key integer,
   state_name varchar(50),
   total integer,
   violent integer,
   homicides integer,
   household_crimes integer,
   rape integer,
   general_homicides integer,
   injuries integer,
   other_crimes integer,
   kidnap integer,
   common_thief integer,
   cattle_thief integer,
   banking_thief integer,
   highway_thief integer,
   no_violent integer,
   primary key(state_key,year));

.separator ","
.import crime.csv crime

CREATE TABLE economic_activity 
   (year integer,
   state_key integer,
   state_name varchar(50), 
   primary_activities integer,
   secondary_activities integer,
   tertiary_activities integer,
   financial_services integer,
   total integer, 
   foreign key(state_key,year)
   references crime (state_key,year));
 
.separator ","
.import economic_activity_by_type.csv economic_activity
DELETE FROM economic_activity WHERE state_key == "State_ID";

CREATE TABLE strikes
   (year integer,
   state_key integer,
   state_name varchar(50),
   number_strikes integer,
   foreign key(state_key,year)
   references crime (state_key,year));

.separator ","
.import strikes.csv strikes
DELETE FROM strikes WHERE state_key == "State_ID";

CREATE TABLE employment
  (year integer,
   state_key varchar(2),
   state_name varchar(50),
   pop_14_and_more integer,
   pop_14_and_more_econ integer,
   employed_pop integer,
   employed_pop_men integer,
   employed_pop_woman integer,
   unemployed_pop integer,
   unemployed_pop_men integer,
   unemployed_pop_woman integer,
   pop_14_and_more_non_econ integer,
   available_pop integer,
   non_available_pop integer,
   foreign key(state_key,year)
   references crime (state_key,year));

.separator ","
.import employment.csv employment
DELETE FROM employment WHERE state_key == "State_ID";


CREATE TABLE urbanization 
   (year integer,
   state_key varchar(2),
   state_name varchar(50),
   number_credits integer,
   investment_household integer,
   water_sources integer,
   treatment_plants integer,
   water_capacity integer,
   volum_water integer,
   intubated_water integer,
   household_water_sources integer,
   localities_water integer,
   drainage_sewage integer,
   localities_drainage_sewage integer,
   sources_electric_energy integer,
   localities_sources_electric_energy integer,
   parks integer,
   gardens integer,
   dam_capacity integer,
   useful_dam_capacity integer,
   used_dam_volume integer,
   foreign key(state_key,year)
   references crime (state_key,year));

.separator ","
.import urbanization.csv urbanization
DELETE FROM urbanization WHERE state_key == "State_ID";

CREATE TABLE justice_system
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   suspects_common_crimes integer,
   sentenced_common_crimes integer,
   suspects_federal_crimes integer,
   sentenced_federal_crimes integer,
   rate_sentenced integer,
   rate_sentenced_federal integer,
   rate_sentenced_common integer,
   used_dam_volume integer,
   foreign key(state_key,year)
   references crime (state_key,year));

.separator ","
.import justice_system.csv justice_system
DELETE FROM justice_system WHERE state_key == "State_ID";


CREATE TABLE cars
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   number_cars integer,
   foreign key(state_key,year)
   references crime (state_key,year));

.separator ","
.import cars.csv cars
DELETE FROM cars WHERE state_key == "State_ID";

