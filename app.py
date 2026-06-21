import streamlit as st
import sqlite3
from datetime import date

conn = sqlite3.connect("journal.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY,
    entry_date TEXT,
    mood TEXT,
    text TEXT
)
""")

st.title("My Journal")

mood = st.selectbox("Mood", ["Happy","Neutral","Sad","Angry"])
entry = st.text_area("Write here")

if st.button("Save"):
    c.execute(
        "INSERT INTO journal(entry_date,mood,text) VALUES(?,?,?)",
        (str(date.today()), mood, entry)
    )
    conn.commit()
    st.success("Saved!")

data = c.execute("SELECT * FROM journal ORDER BY id DESC").fetchall()

for row in data:
    st.write(row[1], row[2])
    st.write(row[3])
