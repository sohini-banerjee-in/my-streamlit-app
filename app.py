import streamlit as st
from supabase import create_client

# Connect to Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("My Journal")

mood = st.selectbox(
    "Mood",
    ["Happy", "Neutral", "Sad", "Angry"]
)

entry = st.text_area("Write here")

if st.button("Save"):
    if entry.strip():
        supabase.table("journal").insert({
            "mood": mood,
            "entry": entry
        }).execute()

        st.success("Saved!")
    else:
        st.warning("Please write something first.")

# Load entries
response = (
    supabase.table("journal")
    .select("*")
    .order("created_at", desc=True)
    .execute()
)

st.subheader("Previous Entries")

for row in response.data:
    st.write(f"📅 {row['created_at'][:10]} | 😊 {row['mood']}")
    st.write(row["entry"])
    st.divider()
