--MINI BASE QUERIES

SELECT  FROM crime c
JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key
JOIN employment e ON c.year = e.year AND c.state_key = e.state_key 
JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key
JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key
JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key
JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key;

--Query for Front-End
SELECT c.year,c.state_key,c.state_name,c.homicides,c.common_thief,c.household_crimes,
ca.number_cars,js.suspects_federal_crimes,s.number_strikes,
ea.primary_activities,e.employed_pop,e.unemployed_pop,
js.rate_sentenced FROM crime c
JOIN economic_activity ea ON ea.year = c.year AND ea.state_key = c.state_key
JOIN employment e ON c.year = e.year AND c.state_key = e.state_key 
JOIN urbanization u ON c.year = u.year AND c.state_key = u.state_key
JOIN justice_system js ON c.year = js.year AND c.state_key = js.state_key
JOIN cars ca ON c.year = ca.year AND c.state_key = ca.state_key
JOIN strikes s ON c.year = s.year AND c.state_key = s.state_key;




 