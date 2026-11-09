SELECT
	track_index,
	start_tick,
	ROUND(MIN(start_seconds), 3) AS time_seconds,
	COUNT(DISTINCT note_number) AS pitch_count
FROM midi_notes
GROUP BY track_index, start_tick
HAVING COUNT(DISTINCT note_number) >= 3
ORDER BY start_tick, track_index;