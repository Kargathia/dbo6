SELECT "datetime"::date, SUM(COUNT(DISTINCT(sql_vragen_nr)))
OVER (ORDER BY "datetime"::date)
FROM gebruiker_activiteit
WHERE status = 'correct'
AND gebruiker_nr = 200
GROUP BY "datetime"::date;

-- Verification: check total number of correct answers by 
-- SELECT COUNT(*) from gebruiker_activiteit
-- WHERE status = 'correct'
-- AND gebruiker_nr = 200;

-- SELECT pcn, nr from gebruiker WHERE nr = 200;