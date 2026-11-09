from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st
import altair as alt

folder = Path(__file__).resolve().parent
database = folder / "midi_project_final.db"
query = (folder / "activity_timeline.sql").read_text(encoding="utf-8-sig")

with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
    activity = pd.read_sql_query(query, connection)

activity["track"] = "Track " + activity["track_index"].astype(str)

st.title("Piano Performance Explorer")
st.subheader("Note starts over time")
st.line_chart(
    activity,
    x="interval_start",
    y="note_count",
    color="track",
    x_label="Start of 10-second interval (seconds)",
    y_label="Note starts",
)
st.dataframe(activity)


with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
    pitch_sql = (folder / "pitch_comparison.sql").read_text(encoding="utf-8-sig")
    pitches = pd.read_sql_query(pitch_sql, connection)

    dynamics_sql = (folder / "track_dynamics.sql").read_text(encoding="utf-8-sig")
    dynamics = pd.read_sql_query(dynamics_sql, connection)

st.subheader("Most-played pitches")
tracks = sorted(pitches["track_index"].unique())
selected_track = st.segmented_control(
    "Choose a track",
    tracks,
    default=tracks[0],
    format_func=lambda track: f"Track {track}",
)

if selected_track is not None:
    top_pitches = pitches[pitches["track_index"] == selected_track].head(10)
    st.bar_chart(
        top_pitches,
        x="note_name",
        y="times_played",
        horizontal=True,
        sort="-times_played",
        x_label="Note starts",
        y_label="Pitch",
        alt="Ten most-played pitches for the selected track",
    )

st.subheader("Average note duration by track")
dynamics["track"] = "Track " + dynamics["track_index"].astype(str)
st.bar_chart(
    dynamics,
    x="track",
    y="avg_duration_seconds",
    x_label="Track",
    y_label="Average note duration (seconds)",
    alt="Average note duration for each piano track",
)
st.subheader("Interactive piano roll")
st.caption("Scroll to zoom in time, drag to pan, and hover over a note for details.")

piano_roll_sql = """
SELECT
    'Track ' || track_index AS track,
    note_number,
    note_name,
    start_seconds,
    duration_seconds,
    start_seconds + duration_seconds AS end_seconds,
    velocity
FROM midi_notes
"""

with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
    piano_roll = pd.read_sql_query(piano_roll_sql, connection)

time_zoom = alt.selection_interval(bind="scales", encodings=["x"])

chart = (
    alt.Chart(piano_roll)
    .mark_bar(size=5, opacity=0.85, cornerRadius=2)
    .encode(
        x=alt.X("start_seconds:Q", title="Time (seconds)"),
        x2="end_seconds:Q",
        y=alt.Y("note_number:Q", title="MIDI pitch", scale=alt.Scale(zero=False)),
        color=alt.Color(
            "track:N",
            title="Piano track",
            scale=alt.Scale(range=["#4F83F1", "#D96C27"]),
        ),
        tooltip=[
            alt.Tooltip("track:N", title="Track"),
            alt.Tooltip("note_name:N", title="Note"),
            alt.Tooltip("start_seconds:Q", title="Start (s)", format=".2f"),
            alt.Tooltip("duration_seconds:Q", title="Duration (s)", format=".2f"),
            alt.Tooltip("velocity:Q", title="MIDI velocity"),
        ],
    )
    .add_params(time_zoom)
    .properties(height=400)
)

st.altair_chart(chart, alt="Piano notes plotted by time and pitch, colored by track")