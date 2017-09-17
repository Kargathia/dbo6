SELECT 
  name, 
  COUNT(name), 
  string_agg(city_id, ',' order by city_id) as id_list
FROM city
GROUP BY name
HAVING (COUNT(name) > 1);

SELECT 
  municipality_id, 
  COUNT(municipality_id), 
  string_agg(name, ',' order by name) as name_list
FROM municipality
GROUP BY municipality_id
HAVING(COUNT(municipality_id) > 1);

SELECT 
  name, 
  COUNT(name), 
  string_agg(code, ',' order by code) as code_list
FROM province
GROUP BY name
HAVING (COUNT(name) > 1);

