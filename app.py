import streamlit as st
from supabase import create_client

# ---------------------------
# Supabase connection
# ---------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.title("📝 My Journal")

# ---------------------------
# Sidebar auth
# ---------------------------
auth_mode = st.sidebar.radio("Account", ["Login", "Sign Up"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# ---------------------------
# Sign up
# ---------------------------
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

# ---------------------------
# Login
# ---------------------------
if auth_mode == "Login":
    if st.sidebar.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state["user"] = result.user
            st.sidebar.success("Logged in!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(str(e))

# ---------------------------
# Current user
# ---------------------------
user = st.session_state.get("user")

# ---------------------------
# Journal input
# ---------------------------
if user:
    st.subheader("Write a new entry")

    mood = st.selectbox("Mood", ["Happy", "Neutral", "Sad", "Angry"])
    entry = st.text_area("Write here")

    if st.button("Save"):
        if entry.strip():
            supabase.table("journal").insert({
                "mood": mood,
                "entry": entry,
                "user_id": user.id
            }).execute()

            st.success("Saved!")
            st.rerun()
        else:
            st.warning("Write something first.")
else:
    st.info("Login to start journaling.")

# ---------------------------
# Load entries (user-specific)
# ---------------------------
if user:
    st.subheader("Your Entries")

    response = (
        supabase.table("journal")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .execute()
    )

    if response.data:
        for row in response.data:
            st.write(f"📅 {row['created_at'][:10]} | 😊 {row['mood']}")
            st.write(row["entry"])

            if st.button("Delete", key=f"del_{row['id']}"):
                supabase.table("journal").delete().eq("id", row["id"]).execute()
                st.rerun()

            st.divider()
    else:
        st.info("No entries yet. Your emotional void is currently empty.")
