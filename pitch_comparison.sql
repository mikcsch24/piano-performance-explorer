SELECT
	track_index,
	note_number,
	note_name,
	COUNT(*) AS times_played
FROM midi_notes
GROUP BY track_index, note_number, note_name
ORDER BY track_index, times_played DESC, note_number;