SELECT 
    COUNT(DISTINCT(gebruiker_activiteit.gebruiker_nr)) as unique_visitors, 
    gebruiker_activiteit."datetime"::date as day
FROM gebruiker_activiteit
GROUP BY day
ORDER BY day