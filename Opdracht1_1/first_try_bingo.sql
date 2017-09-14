SELECT act_1.sql_vragen_nr, gebruiker."displayName", gebruiker.pcn, act_1.status, act_1."datetime"
FROM gebruiker_activiteit act_1
INNER JOIN gebruiker ON act_1.gebruiker_nr = gebruiker.nr
WHERE NOT EXISTS (SELECT * FROM gebruiker_activiteit act_2
                    WHERE act_1.gebruiker_nr = act_2.gebruiker_nr
                    AND act_1.sql_vragen_nr = act_2.sql_vragen_nr
                    AND act_2."datetime" < act_1."datetime")
AND act_1.status = 'correct'
ORDER BY act_1.sql_vragen_nr, gebruiker.pcn

-- SELECT * FROM sql_vragen WHERE nr = 2;