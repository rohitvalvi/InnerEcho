from huggingface_hub import InferenceClient
import streamlit as st
from datetime import datetime, date, timedelta

EMOTION_MODEL = "bhadresh-savani/distilbert-base-uncased-emotion"
CHAT_MODEL    = "mistralai/Mistral-7B-Instruct-v0.3"

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "hurt myself",
    "self harm", "self-harm", "end it all", "want to die", "no reason to live",
]

@st.cache_resource
def _get_client() -> InferenceClient:
    # New HuggingFace router endpoint (api-inference.huggingface.co is discontinued)
    return InferenceClient(
        token=st.secrets["hf_token"],
        base_url="https://router.huggingface.co"
    )


def check_crisis(text: str) -> bool:
    return any(keyword in text.lower() for keyword in CRISIS_KEYWORDS)


def get_emotion(text: str) -> tuple[str, float]:
    try:
        import requests
        # Call new router endpoint directly for text classification
        headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}
        payload = {"inputs": text}
        response = requests.post(
            f"https://router.huggingface.co/hf-inference/models/{EMOTION_MODEL}",
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()
        # Result is [[{label, score}, ...]]
        if isinstance(results, list) and isinstance(results[0], list):
            results = results[0]
        top = sorted(results, key=lambda x: x["score"], reverse=True)[0]
        return top["label"], top["score"]
    except Exception as e:
        return "neutral", 0.5


def get_ai_response(user_message: str, emotion: str, chat_history: list | None = None) -> str:
    system_prompt = (
        "You are InnerEcho, a warm, empathetic, and non-judgmental mental health companion. "
        "Your role is to provide emotional support, active listening, and gentle encouragement. "
        f"The user's current detected emotion is: {emotion}. "
        "Tailor your response accordingly. Keep replies concise (2-4 sentences), "
        "compassionate, and conversational. "
        "Never diagnose or replace professional help. "
        "If the user seems in crisis, gently guide them to emergency resources. "
        "Do NOT use bullet points or lists. Respond naturally like a caring friend."
    )

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        for msg in chat_history[-6:]:
            if msg["role"] in ("user", "assistant"):
                messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        import requests
        headers = {
            "Authorization": f"Bearer {st.secrets['hf_token']}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": CHAT_MODEL,
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.8,
        }
        response = requests.post(
            "https://router.huggingface.co/novita/v3/openai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return reply

    except Exception as e:
        st.error(f"AI response error: {e}")
        fallbacks = {
            "sadness":  "I'm so sorry you're feeling this way. I'm here to listen — would you like to talk more?",
            "joy":      "That sounds wonderful! I'm genuinely happy for you. What made this moment special?",
            "fear":     "It's completely okay to feel anxious. Take a slow, deep breath — I'm right here with you.",
            "anger":    "It sounds like you're really frustrated, and that's completely valid. What's been on your mind?",
            "love":     "That's such a heartwarming feeling. Thank you for sharing that with me.",
            "surprise": "Wow, that sounds unexpected! How are you processing everything?",
            "neutral":  "Thank you for sharing that with me. I'm here — tell me more about how you're feeling.",
        }
        return fallbacks.get(emotion.lower(), "Thank you for sharing that with me. I'm here for you.")


def update_streak() -> None:
    today        = date.today().isoformat()
    last_checkin = st.session_state.get("last_checkin_date")
    streak       = st.session_state.get("streak", 0)

    if last_checkin == today:
        return

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    if last_checkin == yesterday:
        streak += 1
    else:
        streak = 1

    st.session_state["streak"]            = streak
    st.session_state["last_checkin_date"] = today


def save_mood_entry(emotion: str, score: float) -> None:
    import json
    import os

    MOOD_FILE = "data/mood_log.json"
    os.makedirs("data", exist_ok=True)

    new_entry = {
        "Date":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Score": round(score, 2),
        "Mood":  emotion.capitalize(),
    }

    if "mood_data" not in st.session_state:
        st.session_state.mood_data = []
    st.session_state.mood_data.append(new_entry)

    existing = []
    if os.path.exists(MOOD_FILE):
        try:
            with open(MOOD_FILE, "r") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing = []
    existing.append(new_entry)
    with open(MOOD_FILE, "w") as f:
        json.dump(existing, f, indent=2)