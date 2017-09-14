SELECT gebruiker.nr, "displayName", COUNT(DISTINCT(sql_vragen.nr)) as correct
FROM gebruiker
INNER JOIN gebruiker_activiteit ON gebruiker.nr = gebruiker_activiteit.gebruiker_nr
INNER JOIN sql_vragen ON gebruiker_activiteit.sql_vragen_nr = sql_vragen.nr
WHERE gebruiker_activiteit.status = 'correct'
GROUP BY gebruiker.nr
ORDER BY correct DESC
LIMIT 1