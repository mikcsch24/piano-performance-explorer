# Piano Performance Explorer

A SQL and Streamlit case study comparing 941 notes across two piano tracks. Open `index.html` for the project page.

## Run the interactive dashboard

Place your local `midi_project_final.db` next to `dashboard.py`. It should contain the `midi_notes` table imported from your EditMIDI CSV. Then run:

```sh
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py
```

## SQL queries

- `activity_timeline.sql` counts starts per track in ten-second intervals.
- `pitch_comparison.sql` ranks pitches by frequency.
- `track_dynamics.sql` compares duration and velocity.
- `simultaneous_pitches.sql` finds groups of pitches with the same start tick.
- `high_velocity_notes_by_track.sql` joins note rows to track display labels.


