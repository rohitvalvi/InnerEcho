import streamlit as st
from modules.theme import theme
from modules.ai_engine import check_crisis, get_emotion, get_ai_response, save_mood_entry, update_streak

st.markdown(theme(), unsafe_allow_html=True)

st.header("Companion Chat")
st.caption("A safe, judgment-free space. Share what's on your mind.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("How are you feeling right now?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if check_crisis(prompt):
        crisis_msg = (
            "I'm really concerned about what you've shared. "
            "Please know you're not alone — help is available right now.\n\n"
            "**iCall (National):** 9152987821 *(Mon–Sat, 8am–10pm)*\n\n"
            "**Vandrevala Foundation:** 9999666555 *(24/7)*\n\n"
            "Would you like to visit the Emergency page for more support options?"
        )
        with st.chat_message("assistant"):
            st.error("Crisis support resources shown above.")
            st.markdown(crisis_msg)
        st.session_state.messages.append({"role": "assistant", "content": crisis_msg})

    else:
        with st.spinner("Thinking..."):
            emotion, score = get_emotion(prompt)
            response = get_ai_response(
                user_message=prompt,
                emotion=emotion,
                chat_history=st.session_state.messages[:-1],
            )

        save_mood_entry(emotion, score)
        update_streak()

        with st.chat_message("assistant"):
            st.caption(f"Detected mood: **{emotion.capitalize()}** ({int(score * 100)}% confidence)")
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if st.session_state.get("messages"):
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()