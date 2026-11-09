SELECT
	track_index,
	CAST(start_seconds / 10.0 AS INTEGER) * 10 AS interval_start,
	COUNT(*) AS note_count
	FROM midi_notes
	GROUP BY track_index, interval_start
	ORDER BY interval_start, track_index;