-- DEPENDENT VARIABLE (CRIME)
-- COVARIATES
CREATE TABLE economic_activity 
   (year integer,
   state_key integer,
   state_name varchar(50), 
   primary_activities integer,
   secondary_activities integer,
   tertiary_activities integer,
   financial_services integer,
   total integer, 
   primary key(state_key,year));

.separator ","
.import economic_activity_by_type.csv economic_activity
DELETE FROM economic_activity WHERE state_key == "State_ID";

CREATE TABLE strikes
   (year integer,
   state_key integer,
   state_name varchar(50),
   number_strikes integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

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
   references economic_activity (state_key,year));

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
   references economic_activity (state_key,year));

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
   references economic_activity (state_key,year));

.separator ","
.import justice_system.csv justice_system
DELETE FROM justice_system WHERE state_key == "State_ID";


CREATE TABLE cars
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   number_cars integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import number_cars.csv cars
DELETE FROM cars WHERE state_key == "State_ID";


CREATE TABLE deaths_registered_doctors
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   deaths_registered_doctors integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import deaths_registered_doctors.csv deaths_registered_doctors
DELETE FROM deaths_registered_doctors WHERE state_key == "State_ID";


CREATE TABLE education_1
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   attended_population integer,
   number_teachers integer,
   child_development_centers integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import education_1.csv education_1
DELETE FROM education_1 WHERE state_key == "State_ID";


CREATE TABLE education_2
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   students_basic_secondary integer,
   approved_students_basic_secondary integer,
   graduate_students_basic_secondary integer,
   teachers_basic_secondary integer,
   schools_basic_secondary integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import education_2.csv education_2
DELETE FROM education_2 WHERE state_key == "State_ID";


CREATE TABLE education_3
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   attended_population_child_centers integer,
   teachers_child_centers integer,
   child_development_centers integer,
   retention_primary_school number,
   academic_achievement_primary number,
   retention_middle_school number, 
   academic_achievement_middle number,
   retention_high_school number,
   academic_achievement_high number,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import education_3.csv education_3
DELETE FROM education_3 WHERE state_key == "State_ID";


CREATE TABLE education_4
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   enrolled_students_indigenous_school integer,
   students_indigenous_school integer,
   approved_students_indigenous_school integer,
   graduate_students_indigenous_school integer,
   teachers_indigenous_school integer,
   indigenous_primary_schools integer,
   active_students_open_highschool integer,
   graduate_students_open_highschool integer,
   foreign key(state_key,year)
   references economic_activity (state_key,year));

.separator ","
.import education_4.csv education_4
DELETE FROM education_4 WHERE state_key == "State_ID";


CREATE TABLE education_5
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   literate_adults integer,
   literate_adults_men integer,
   literate_adults_women integer,
   literacy_teachers integer,
   adults_primary_school integer,
   primary_school_certificates integer,
   adults_middle_school integer,
   middle_school_certificates integer,
   enrolled_students_work_training integer,
   students_work_training integer,
   accredited_students_work_training integer,
   teachers_work_training integer,
   schools_work_training integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import education_5.csv education_5
DELETE FROM education_5 WHERE state_key == "State_ID";


CREATE TABLE education_6
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   number_campuses integer,
   number_classrooms integer,
   number_libraries integer,
   number_laboratories integer,
   number_studios integer,
   number_annexes integer,
   number_public_libraries integer,
   employees_public_libraries integer,
   titles_public_libraries integer,
   books_public_libraries integer,
   library_consultations integer,
   users_public_libraries integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import education_6.csv education_6
DELETE FROM education_6 WHERE state_key == "State_ID";


CREATE TABLE enviroment
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   trees_planted integer,
   reforested_area integer,
   garbage_collection integer,
   environmental_complaints integer,
   environmental_licenses integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import enviroment.csv enviroment
DELETE FROM enviroment WHERE state_key == "State_ID";


CREATE TABLE health
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   social_security_beneficiaries integer,
   social_security_users integer,
   benefited_families integer, 
   social_security_affiliates integer,
   external_consultations integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import health.csv health
DELETE FROM health WHERE state_key == "State_ID";


CREATE TABLE health_1
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   consultations_per_doctor number,
   consultations_per_unit number,
   doctors_per_unit number,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import health_1.csv health_1
DELETE FROM health_1 WHERE state_key == "State_ID";


CREATE TABLE justice_system_1
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   common_crime_agencies integer,
   federal_crimes_agencies integer,
   common_crimes_prosecutors integer,
   federal_crimes_prosecutors integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import justice_system_1.csv justice_system_1
DELETE FROM justice_system_1 WHERE state_key == "State_ID";


CREATE TABLE justice_system_2
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   number_accidents integer,
   car_crash integer,
   pedestrian_crash integer,
   object_crash integer,
   others_crashes integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import justice_system_2.csv justice_system_2
DELETE FROM justice_system_2 WHERE state_key == "State_ID";


CREATE TABLE justice_system_3
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   common_crime_agencies integer,
   federal_crimes_agencies integer,
   capacity_penitentiary_centers integer,
   total_inmmates integer,
   common_crimes_inmates integer,
   common_crimes_inmates_men integer,
   common_crimes_inmates_women integer,
   federal_crimes_inmates integer,
   federal_crimes_men integer,
   federal_crimes_inmates_women integer,
   total_inmates1 integer,
   total_inmates_men integer,
   total_inmates_woman integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import justice_system_3.csv justice_system_3
DELETE FROM justice_system_3 WHERE state_key == "State_ID";


CREATE TABLE percentage_jungle_forest
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   area_forests_jungles number,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import percentage_jungle_forest.csv percentage_jungle_forest
DELETE FROM percentage_jungle_forest WHERE state_key == "State_ID";


CREATE TABLE state_income_expenditure
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   state_income float, 
   state_expenditure float,  
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import state_income_expenditure.csv state_income_expenditure
DELETE FROM state_income_expenditure WHERE state_key == "State_ID";


CREATE TABLE total_population
   (year integer,
   state_key varchar(3),
   state_name varchar(50),
   total_population integer,
   population_small_localities integer,
   population_large_localities integer,
   not_applicable integer,
   foreign key(state_key,year) 
   references economic_activity (state_key,year));

.separator ","
.import total_population.csv total_population
DELETE FROM total_population WHERE state_key == "State_ID";