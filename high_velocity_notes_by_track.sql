WITH tracks(track_index, display_name) AS (
    VALUES (1, 'Piano (track 1)'),
           (2, 'Piano (track 2)')
)
SELECT
    t.display_name,
    COUNT(*) AS high_velocity_notes
FROM midi_notes AS n
INNER JOIN tracks AS t
    ON n.track_index = t.track_index
WHERE n.velocity >= 90
GROUP BY t.track_index, t.display_name
ORDER BY t.track_index;