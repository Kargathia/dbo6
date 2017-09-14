SELECT DISTINCT(act_1.sql_vragen_nr) from gebruiker_activiteit act_1
WHERE gebruiker_nr = 200 
AND sql_vragen_nr NOT IN (
    SELECT DISTINCT(sql_vragen_nr) from gebruiker_activiteit
    WHERE gebruiker_nr = act_1.gebruiker_nr
    AND status = 'correct'
);

SELECT correct_answ.num as questions_correct, all_answ.num as questions_answered
FROM
    (SELECT COUNT(DISTINCT(sql_vragen_nr)) as num
    FROM gebruiker_activiteit
    WHERE gebruiker_nr = 200
    AND status = 'correct'
    ) correct_answ,
    
    (SELECT COUNT(DISTINCT(sql_vragen_nr)) as num
    FROM gebruiker_activiteit
    WHERE gebruiker_nr = 200
    ) all_answ