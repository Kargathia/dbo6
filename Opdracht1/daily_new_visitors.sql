SELECT COUNT(gebruiker.nr), gebruiker.aangemaakt::date
FROM gebruiker
GROUP BY gebruiker.aangemaakt::date
ORDER BY gebruiker.aangemaakt::date
LIMIT 20;