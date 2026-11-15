SELECT
    CASE result
        WHEN 'H' THEN 'Home Win'
        WHEN 'D' THEN 'Draw'
        WHEN 'A' THEN 'Away Win'
    END AS outcome,
    COUNT(*) AS matches,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM matches
GROUP BY result
ORDER BY matches DESC;