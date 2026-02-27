import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
import io
import base64
from modules.theme import theme

st.markdown(theme(), unsafe_allow_html=True)

st.title("My Profile")
st.caption("Your personal space — tell InnerEcho a little about yourself.")

PROFILE_FILE = "data/profile.json"
os.makedirs("data", exist_ok=True)

def load_profile() -> dict:
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}

def save_profile(data: dict) -> None:
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")

def base64_to_image(b64_str: str):
    return Image.open(io.BytesIO(base64.b64decode(b64_str)))

profile = load_profile()

# ── Avatar + Name banner ──────────────────────────────────────────────────────
avatar_col, info_col = st.columns([1, 3])

with avatar_col:
    if profile.get("avatar"):
        try:
            st.image(base64_to_image(profile["avatar"]), width=130)
        except Exception:
            st.image("https://api.dicebear.com/7.x/thumbs/svg?seed=innerecho", width=130)
    else:
        st.image("https://api.dicebear.com/7.x/thumbs/svg?seed=innerecho", width=130)

with info_col:
    st.markdown(f"## {profile.get('name', 'Your Name')}")
    st.markdown(
        f"**Age:** {profile.get('age', '—')}  &nbsp;&nbsp;  "
        f"**Gender:** {profile.get('gender', '—')}  &nbsp;&nbsp;  "
        f"**Member since:** {profile.get('member_since', datetime.now().strftime('%Y-%m-%d'))}"
    )
    streak = st.session_state.get("streak", 0)
    st.markdown(f"**Check-in Streak:** {streak} day{'s' if streak != 1 else ''}")
    if profile.get("bio"):
        st.caption(f"*\"{profile['bio']}\"*")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["Edit Profile", "Mental Health Goals", "Emergency Contacts", "Interests & Hobbies"])

# ── Tab 1: Edit Profile ───────────────────────────────────────────────────────
with tab1:
    st.subheader("Personal Details")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", value=profile.get("name", ""), placeholder="e.g. Aarav Sharma")
        age  = st.number_input("Age", min_value=10, max_value=100, value=int(profile.get("age", 18)))
    with col2:
        GENDER_OPTIONS = ["Prefer not to say", "Male", "Female", "Non-binary", "Other"]
        gender   = st.selectbox("Gender", GENDER_OPTIONS, index=GENDER_OPTIONS.index(profile.get("gender", "Prefer not to say")))
        pronouns = st.text_input("Pronouns (optional)", value=profile.get("pronouns", ""), placeholder="e.g. she/her, he/him")

    bio = st.text_area("Short Bio (optional)", value=profile.get("bio", ""), height=90, placeholder="A little about yourself...")

    st.subheader("Profile Photo")
    uploaded_photo = st.file_uploader("Upload a profile photo", type=["png", "jpg", "jpeg"])

    if st.button("Save Profile"):
        updated = {
            **profile,
            "name":         name.strip() or "Your Name",
            "age":          age,
            "gender":       gender,
            "pronouns":     pronouns.strip(),
            "bio":          bio.strip(),
            "member_since": profile.get("member_since", datetime.now().strftime("%Y-%m-%d")),
        }
        if uploaded_photo is not None:
            updated["avatar"] = image_to_base64(uploaded_photo.read())
        save_profile(updated)
        st.toast("Profile saved.")
        st.rerun()

    st.divider()
    st.subheader("Check-in Streak")
    streak = st.session_state.get("streak", 0)
    st.metric("Current Streak", f"{streak} day{'s' if streak != 1 else ''}")

    if streak >= 7:
        st.success("One week strong! You're doing amazing.")
    elif streak >= 3:
        st.info("Great consistency! You're building a healthy habit.")
    elif streak >= 1:
        st.info("Good start! Come back tomorrow to grow your streak.")
    else:
        st.warning("Chat with your Companion daily to start your streak.")

# ── Tab 2: Mental Health Goals ────────────────────────────────────────────────
with tab2:
    st.subheader("My Mental Health Goals")
    st.caption("Set intentions to guide your well-being journey.")

    goals: list = profile.get("goals", [])

    new_goal = st.text_input("Add a new goal", placeholder="e.g. Practice mindfulness for 10 minutes daily", key="new_goal_input")
    if st.button("Add Goal"):
        if new_goal.strip():
            goals.append({"text": new_goal.strip(), "done": False, "added": datetime.now().strftime("%Y-%m-%d")})
            profile["goals"] = goals
            save_profile(profile)
            st.toast("Goal added.")
            st.rerun()
        else:
            st.warning("Please type a goal before adding.")

    st.divider()

    if not goals:
        st.info("No goals yet — add one above to get started.")
    else:
        for i, goal in enumerate(goals):
            gcol1, gcol2, gcol3 = st.columns([0.5, 6, 0.8])
            with gcol1:
                checked = st.checkbox("", value=goal["done"], key=f"goal_{i}")
                if checked != goal["done"]:
                    goals[i]["done"] = checked
                    profile["goals"] = goals
                    save_profile(profile)
                    st.rerun()
            with gcol2:
                display = f"~~{goal['text']}~~" if goal["done"] else goal["text"]
                st.markdown(f"{display}  \n*Added {goal.get('added', '')}*")
            with gcol3:
                if st.button("Delete", key=f"del_goal_{i}"):
                    goals.pop(i)
                    profile["goals"] = goals
                    save_profile(profile)
                    st.rerun()

        completed = sum(1 for g in goals if g["done"])
        st.caption(f"{completed} / {len(goals)} completed")
        st.progress(completed / len(goals) if goals else 0)

# ── Tab 3: Emergency Contacts ─────────────────────────────────────────────────
with tab3:
    st.subheader("Emergency Contacts")
    st.caption("These people will be alerted when you send an SOS from the Emergency page.")

    contacts: list = profile.get("emergency_contacts", [])

    with st.expander("Add New Contact", expanded=len(contacts) == 0):
        cc1, cc2 = st.columns(2)
        with cc1:
            c_name     = st.text_input("Name",         placeholder="e.g. Ankit Shelar", key="c_name")
            c_relation = st.text_input("Relationship", placeholder="e.g. Mother, Friend", key="c_rel")
        with cc2:
            c_phone = st.text_input("Phone Number",     placeholder="e.g. 9876456770",    key="c_phone")
            c_email = st.text_input("Email (optional)", placeholder="e.g. ankit@email.com",key="c_email")

        if st.button("Save Contact"):
            if c_name.strip() and c_phone.strip():
                contacts.append({"name": c_name.strip(), "relation": c_relation.strip(), "phone": c_phone.strip(), "email": c_email.strip()})
                profile["emergency_contacts"] = contacts
                save_profile(profile)
                st.toast(f"{c_name} added as emergency contact.")
                st.rerun()
            else:
                st.warning("Name and phone number are required.")

    st.divider()

    if not contacts:
        st.info("No emergency contacts saved yet.")
    else:
        for i, contact in enumerate(contacts):
            ec1, ec2 = st.columns([5, 1])
            with ec1:
                email_str = f"  |  {contact['email']}" if contact.get("email") else ""
                st.markdown(f"**{contact['name']}**  ·  *{contact.get('relation', 'Contact')}*\n\n{contact['phone']}{email_str}")
            with ec2:
                if st.button("Remove", key=f"del_c_{i}"):
                    contacts.pop(i)
                    profile["emergency_contacts"] = contacts
                    save_profile(profile)
                    st.toast("Contact removed.")
                    st.rerun()
            st.markdown("---")

# ── Tab 4: Interests & Hobbies ────────────────────────────────────────────────
with tab4:
    st.subheader("Interests & Hobbies")
    st.caption("Help InnerEcho know you better — these make your experience more personal.")

    st.markdown("#### Hobbies")
    HOBBY_SUGGESTIONS = ["Reading", "Drawing / Painting", "Gaming", "Cooking", "Yoga / Meditation",
                         "Photography", "Journaling", "Gardening", "Hiking", "Music", "Dancing", "Travelling"]
    saved_hobbies = profile.get("hobbies", [])
    hobbies = st.multiselect("Select your hobbies", options=HOBBY_SUGGESTIONS,
                             default=[h for h in saved_hobbies if h in HOBBY_SUGGESTIONS])
    custom_hobby = st.text_input("Add a custom hobby", value=profile.get("custom_hobby", ""), placeholder="e.g. Origami, Rock climbing...")

    st.divider()
    st.markdown("#### Favourite Songs / Artists")
    fav_songs = st.text_area("List your favourite songs or artists", value=profile.get("fav_songs", ""), height=80,
                              placeholder="e.g. Tum Hi Ho – Arijit Singh, Blinding Lights – The Weeknd...")

    MUSIC_GENRES = ["Pop", "Bollywood", "Hip-Hop / Rap", "R&B / Soul", "Rock", "Classical / Instrumental",
                    "Jazz", "Electronic / EDM", "Indie", "Folk / Acoustic", "Metal", "Lo-fi"]
    saved_music = profile.get("music_genres", [])
    music_genres = st.multiselect("Favourite music genres", options=MUSIC_GENRES,
                                  default=[m for m in saved_music if m in MUSIC_GENRES])

    st.divider()
    st.markdown("#### Favourite Movie / Show Genres")
    MOVIE_GENRES = ["Comedy", "Drama", "Romance", "Thriller / Mystery", "Horror", "Sci-Fi",
                    "Fantasy / Adventure", "Action", "Animation", "Documentary", "Biography",
                    "Crime", "Slice of Life", "Anime"]
    saved_movies = profile.get("movie_genres", [])
    movie_genres = st.multiselect("Select your favourite genres", options=MOVIE_GENRES,
                                  default=[m for m in saved_movies if m in MOVIE_GENRES])
    fav_movies = st.text_area("Favourite movies or shows (optional)", value=profile.get("fav_movies", ""), height=80,
                               placeholder="e.g. 3 Idiots, Inception, Friends...")

    st.divider()
    if st.button("Save Interests"):
        profile.update({
            "hobbies":      hobbies,
            "custom_hobby": custom_hobby.strip(),
            "fav_songs":    fav_songs.strip(),
            "music_genres": music_genres,
            "movie_genres": movie_genres,
            "fav_movies":   fav_movies.strip(),
        })
        save_profile(profile)
        st.toast("Interests saved.")
        st.rerun()

    if any([profile.get("hobbies"), profile.get("music_genres"), profile.get("movie_genres"), profile.get("fav_songs")]):
        st.divider()
        st.subheader("Your Interests at a Glance")
        all_hobbies = profile.get("hobbies", []) + ([profile["custom_hobby"]] if profile.get("custom_hobby") else [])
        if all_hobbies:
            st.markdown("**Hobbies:** " + "  ·  ".join(f"`{h}`" for h in all_hobbies))
        if profile.get("music_genres"):
            st.markdown("**Music:** " + "  ·  ".join(f"`{g}`" for g in profile["music_genres"]))
        if profile.get("fav_songs"):
            st.markdown(f"**Favourite Songs/Artists:** {profile['fav_songs']}")
        if profile.get("movie_genres"):
            st.markdown("**Movie Genres:** " + "  ·  ".join(f"`{g}`" for g in profile["movie_genres"]))
        if profile.get("fav_movies"):
            st.markdown(f"**Favourite Movies/Shows:** {profile['fav_movies']}")