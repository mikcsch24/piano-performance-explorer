SELECT
	track_index,
	ROUND(AVG(duration_seconds), 3) AS avg_duration_seconds,
	ROUND(AVG(velocity), 1) AS avg_velocity,
	MIN(velocity) AS min_velocity,
	MAX(velocity) AS max_velocity
FROM midi_notes
GROUP BY track_index
ORDER BY track_index;