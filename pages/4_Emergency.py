import streamlit as st
import time
from modules.theme import theme

st.markdown(theme(), unsafe_allow_html=True)

st.title("Emergency Support")
st.markdown("#### You are not alone. Reaching out is the bravest thing you can do.")

st.error(
    "If you or someone you know is in immediate danger, "
    "please call **112** (India Emergency) or your local emergency number right away."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Crisis Helplines")
    st.info("**iCall (National):** 9152987821\n\n*Mon–Sat, 8am–10pm*")
    st.info("**Vandrevala Foundation:** 9999666555\n\n*24/7 Support*")
    st.info("**Snehi:** 044-24640050\n\n*Mon–Sat, 8am–10pm*")
    st.link_button("Chat with a Professional Online", "https://icallhelpline.org/", use_container_width=True)

with col2:
    st.subheader("Your Guardians")
    st.markdown("These trusted contacts will be alerted if you send an SOS.")
    st.success("**Primary Guardian:** Rohit")
    st.success("**Secondary Guardian:** Rutik")
    st.divider()
    if st.button("Send SOS Alert to Guardians", type="primary", use_container_width=True):
        with st.spinner("Sending SOS alert..."):
            time.sleep(1.5)
        st.warning(
            "SOS alert sent to **Rohit** and **Rutik**.\n\n"
            "They have been notified. Please stay somewhere safe and wait for them to reach out."
        )

st.divider()

st.subheader("Quick Grounding: The 5-4-3-2-1 Technique")
st.markdown(
    "If you're feeling overwhelmed, this exercise brings you back to the present:\n\n"
    "- Name **5 things** you can see around you\n"
    "- Name **4 things** you can physically feel\n"
    "- Name **3 things** you can hear\n"
    "- Name **2 things** you can smell\n"
    "- Name **1 thing** you can taste\n\n"
    "*Take slow, deep breaths as you go through each step. You are safe.*"
)

st.divider()

st.subheader("Additional Resources")
r1, r2, r3 = st.columns(3)
with r1:
    st.link_button("iCall Helpline",        "https://icallhelpline.org/",          use_container_width=True)
with r2:
    st.link_button("Vandrevala Foundation", "https://www.vandrevalafoundation.com/",use_container_width=True)
with r3:
    st.link_button("Find Local Support",    "https://www.findahelpline.com/",       use_container_width=True)

st.divider()
st.caption(
    "InnerEcho is an AI-powered support tool and is NOT a substitute for clinical diagnosis, "
    "therapy, or emergency medical intervention. Always seek professional help when needed."
)