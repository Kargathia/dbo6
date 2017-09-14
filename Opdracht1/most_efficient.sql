SELECT 
    gebruiker.nr,
    "displayName",
    correct.total as correct_total,
    action_total.total as "total actions",
    (cast(correct.total as numeric) / action_total.total) as correct_ratio
from gebruiker

-- Select the number of unique questions that were answered correctly
INNER JOIN (SELECT 
                gebruiker.nr as gebruiker_nr, 
                COUNT(DISTINCT(sql_vragen.nr)) as total
            FROM gebruiker
            INNER JOIN gebruiker_activiteit ON gebruiker.nr = gebruiker_activiteit.gebruiker_nr
            INNER JOIN sql_vragen ON gebruiker_activiteit.sql_vragen_nr = sql_vragen.nr
            WHERE gebruiker_activiteit.status = 'correct'
            GROUP BY gebruiker.nr) correct 
ON (gebruiker.nr = correct.gebruiker_nr)

-- Select the total number wrong answers by user - this does not have to be unique
INNER JOIN (SELECT 
                gebruiker.nr as gebruiker_nr, 
                COUNT(gebruiker_activiteit.nr) as total
            FROM gebruiker
            INNER JOIN gebruiker_activiteit ON gebruiker.nr = gebruiker_activiteit.gebruiker_nr
            GROUP BY gebruiker.nr) action_total 
ON (gebruiker.nr = action_total.gebruiker_nr)

ORDER BY correct_ratio DESC
LIMIT 10