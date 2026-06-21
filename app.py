import streamlit as st
from supabase import create_client

# Connect to Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("My Journal")
auth_mode = st.sidebar.radio(
    "Account",
    ["Login", "Sign Up"]
)

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if auth_mode == "Sign Up":
    if st.sidebar.button("Create Account"):
        try:
            supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            st.sidebar.success("Account created!")
        except Exception as e:
            st.sidebar.error(str(e))

if auth_mode == "Login":
    if st.sidebar.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state["user"] = result.user
            st.sidebar.success("Logged in!")
        except Exception as e:
            st.sidebar.error(str(e))

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
