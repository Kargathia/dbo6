SELECT distinct status, 
       count(nr) as num_queries,
       count(nr) * 100.0 / (select count(nr) from gebruiker_activiteit) as pct
FROM gebruiker_activiteit
group by status