import streamlit as st
import json
import os
import hashlib
from datetime import datetime
from modules.theme import theme

st.markdown(theme(), unsafe_allow_html=True)

DIARY_FILE = "data/diary_entries.json"
AUTH_FILE  = "data/auth.json"
os.makedirs("data", exist_ok=True)

st.title("Personal Diary")
st.caption("Your private, secure space to record your thoughts.")

# ── Helpers ───────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_auth() -> dict:
    if os.path.exists(AUTH_FILE):
        try:
            with open(AUTH_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_auth(data: dict) -> None:
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_password_set() -> bool:
    return bool(load_auth().get("password_hash"))

def verify_password(password: str) -> bool:
    return hash_password(password) == load_auth().get("password_hash", "")

def set_password(password: str) -> None:
    save_auth({"password_hash": hash_password(password)})

@st.cache_data(ttl=1)
def _read_entries() -> list:
    if os.path.exists(DIARY_FILE):
        try:
            with open(DIARY_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def load_entries() -> list:
    return _read_entries()

def save_entries(entries: list) -> None:
    with open(DIARY_FILE, "w") as f:
        json.dump(entries, f, indent=2)
    _read_entries.clear()

# ── Session state ─────────────────────────────────────────────────────────────
if "diary_unlocked" not in st.session_state:
    st.session_state.diary_unlocked = False

# ── First-time setup ──────────────────────────────────────────────────────────
if not is_password_set():
    st.info("Welcome! Create a password to protect your diary.")
    st.divider()
    st.subheader("Create Your Diary Password")
    new_pass     = st.text_input("Choose a password", type="password", placeholder="At least 6 characters")
    confirm_pass = st.text_input("Confirm your password", type="password", placeholder="Repeat your password")

    if st.button("Set Password", use_container_width=True):
        if len(new_pass) < 6:
            st.error("Password must be at least 6 characters.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            set_password(new_pass)
            st.session_state.diary_unlocked = True
            st.success("Password created. Your diary is now protected.")
            st.rerun()
    st.stop()

# ── Login ─────────────────────────────────────────────────────────────────────
if not st.session_state.diary_unlocked:
    st.subheader("Enter Your Password")
    entered = st.text_input("Password", type="password", placeholder="Enter your diary password...")

    col_login, col_forgot = st.columns([2, 1])
    with col_login:
        if st.button("Unlock Diary", use_container_width=True):
            if verify_password(entered):
                st.session_state.diary_unlocked = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    with col_forgot:
        if st.button("Reset Password", use_container_width=True):
            st.session_state.show_reset = True

    if st.session_state.get("show_reset"):
        st.divider()
        st.warning("You will need your current password to set a new one.")
        current = st.text_input("Current password",     type="password", key="reset_current")
        new_p   = st.text_input("New password",          type="password", key="reset_new")
        confirm = st.text_input("Confirm new password",  type="password", key="reset_confirm")

        if st.button("Confirm Reset"):
            if not verify_password(current):
                st.error("Current password is incorrect.")
            elif len(new_p) < 6:
                st.error("New password must be at least 6 characters.")
            elif new_p != confirm:
                st.error("New passwords do not match.")
            else:
                set_password(new_p)
                st.session_state.show_reset = False
                st.success("Password updated. Please log in.")
                st.rerun()
    st.stop()

# ── Sidebar (authenticated) ───────────────────────────────────────────────────
with st.sidebar:
    st.info("Your diary entries are password protected.")
    st.divider()
    if st.button("Lock Diary"):
        st.session_state.diary_unlocked = False
        st.rerun()

    with st.expander("Change Password"):
        old_p  = st.text_input("Current password",    type="password", key="cp_old")
        new_p  = st.text_input("New password",         type="password", key="cp_new")
        conf_p = st.text_input("Confirm new password", type="password", key="cp_conf")
        if st.button("Update Password"):
            if not verify_password(old_p):
                st.error("Current password is wrong.")
            elif len(new_p) < 6:
                st.error("New password too short.")
            elif new_p != conf_p:
                st.error("Passwords do not match.")
            else:
                set_password(new_p)
                st.success("Password updated.")

st.success("Access granted — welcome back!")
st.divider()

# ── New Entry ─────────────────────────────────────────────────────────────────
st.subheader("New Entry")

col1, col2 = st.columns([3, 1])
with col1:
    entry_title = st.text_input("Title (optional)", placeholder="Give your entry a title...")
with col2:
    mood_tag = st.selectbox("Mood", ["Happy", "Sad", "Anxious", "Angry", "Calm", "Reflective", "Tired"])

entry_text = st.text_area("Write your thoughts here...", height=180, placeholder="What's on your mind today?")

if st.button("Save Entry"):
    if not entry_text.strip():
        st.warning("Please write something before saving.")
    else:
        entries = load_entries()
        entries.append({
            "id":      len(entries) + 1,
            "date":    datetime.now().strftime("%Y-%m-%d %H:%M"),
            "title":   entry_title.strip() or "Untitled",
            "mood":    mood_tag,
            "content": entry_text.strip(),
        })
        save_entries(entries)
        st.toast("Diary entry saved.")
        st.rerun()

st.divider()

# ── Past Entries ──────────────────────────────────────────────────────────────
st.subheader("Past Entries")
entries = load_entries()

if not entries:
    st.info("No diary entries yet. Write your first one above.")
else:
    search_query = st.text_input("Search entries", placeholder="Search by title or content...")
    filtered = list(reversed(entries))
    if search_query:
        q = search_query.lower()
        filtered = [e for e in filtered if q in e.get("title", "").lower() or q in e["content"].lower()]

    st.caption(f"Showing {len(filtered)} of {len(entries)} entries")

    for entry in filtered:
        label = f"{entry['mood']}  |  {entry['date']}  |  **{entry.get('title', 'Untitled')}**"
        with st.expander(label):
            st.write(entry["content"])
            if st.button("Delete this entry", key=f"del_{entry['id']}"):
                all_entries = load_entries()
                all_entries = [e for e in all_entries if e["id"] != entry["id"]]
                save_entries(all_entries)
                st.toast("Entry deleted.")
                st.rerun()