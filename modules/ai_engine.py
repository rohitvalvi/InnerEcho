import requests
import streamlit as st
from datetime import datetime, date, timedelta

EMOTION_MODEL = "bhadresh-savani/distilbert-base-uncased-emotion"

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "hurt myself",
    "self harm", "self-harm", "end it all", "want to die", "no reason to live",
]

WELLBEING_BASE = {
    "joy": 0.90,
    "love": 0.85,
    "surprise": 0.65,
    "neutral": 0.55,
    "anger": 0.30,
    "sadness": 0.25,
    "fear": 0.20,
}


def check_crisis(text: str) -> bool:
    return any(keyword in text.lower() for keyword in CRISIS_KEYWORDS)


def _parse_emotion_results(results: object) -> tuple[str, float] | None:
    if isinstance(results, list) and results and isinstance(results[0], list):
        results = results[0]
    if not isinstance(results, list) or not results:
        return None

    valid = [r for r in results if isinstance(r, dict) and "label" in r and "score" in r]
    if not valid:
        return None

    top = max(valid, key=lambda x: float(x.get("score", 0)))
    label = str(top.get("label", "neutral")).lower()
    score = max(0.0, min(1.0, float(top.get("score", 0.5))))
    return label, score


def _emotion_from_keywords(text: str) -> tuple[str, float]:
    t = text.lower()
    if any(k in t for k in ["happy", "great", "excited", "awesome", "glad", "good"]):
        return "joy", 0.65
    if any(k in t for k in ["sad", "down", "cry", "lonely", "empty", "depressed"]):
        return "sadness", 0.70
    if any(k in t for k in ["angry", "mad", "furious", "irritated", "annoyed"]):
        return "anger", 0.70
    if any(k in t for k in ["scared", "afraid", "anxious", "panic", "worried", "nervous"]):
        return "fear", 0.70
    if any(k in t for k in ["love", "grateful", "thankful", "caring", "affection"]):
        return "love", 0.65
    if any(k in t for k in ["wow", "unexpected", "shocked", "surprised"]):
        return "surprise", 0.60
    return "neutral", 0.50


def _emotion_from_groq(text: str) -> tuple[str, float] | None:
    groq_token = st.secrets.get("groq_token")
    if not groq_token:
        return None

    prompt = (
        "Classify the user's emotion into exactly one label from this set: "
        "joy, sadness, fear, anger, love, surprise, neutral. "
        "Return strict JSON with keys label and confidence only. "
        f"User text: {text}"
    )

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {groq_token}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 80,
            "response_format": {"type": "json_object"},
        },
        timeout=15,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    parsed = response.json()

    import json
    data = json.loads(content)
    label = str(data.get("label", "neutral")).lower()
    if label not in WELLBEING_BASE:
        label = "neutral"
    confidence = max(0.0, min(1.0, float(data.get("confidence", 0.5))))
    return label, confidence


def get_emotion(text: str) -> tuple[str, float]:
    hf_token = st.secrets.get("hf_token")
    if hf_token:
        for endpoint in (
            f"https://router.huggingface.co/hf-inference/models/{EMOTION_MODEL}",
            f"https://api-inference.huggingface.co/models/{EMOTION_MODEL}",
        ):
            try:
                response = requests.post(
                    endpoint,
                    headers={"Authorization": f"Bearer {hf_token}"},
                    json={"inputs": text},
                    timeout=12,
                )
                response.raise_for_status()
                parsed = _parse_emotion_results(response.json())
                if parsed:
                    return parsed
            except Exception:
                continue

    try:
        groq_result = _emotion_from_groq(text)
        if groq_result:
            return groq_result
    except Exception:
        pass

    return _emotion_from_keywords(text)


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
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.secrets['groq_token']}",
                "Content-Type":  "application/json",
            },
            json={
                "model":       "llama-3.1-8b-instant",
                "messages":    messages,
                "max_tokens":  300,
                "temperature": 0.8,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

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
    last_checkin = st.session_state.get("last_checkin_date", None)
    streak       = st.session_state.get("streak", 0)

    if last_checkin == today:
        return

    if last_checkin:
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        streak = streak + 1 if last_checkin == yesterday else 1
    else:
        streak = 1

    st.session_state["streak"]            = streak
    st.session_state["last_checkin_date"] = today


def emotion_to_wellbeing(emotion: str, confidence: float) -> float:
    base = WELLBEING_BASE.get(emotion.lower(), 0.50)
    confidence = max(0.0, min(1.0, float(confidence)))
    # Keep uncertain detections close to neutral (0.5) and stronger detections closer to mood baseline.
    return round(0.5 + (base - 0.5) * confidence, 2)


def save_mood_entry(emotion: str, score: float) -> None:
    import json, os

    MOOD_FILE = "data/mood_log.json"
    os.makedirs("data", exist_ok=True)

    confidence = max(0.0, min(1.0, float(score)))
    wellbeing_score = emotion_to_wellbeing(emotion, confidence)

    new_entry = {
        "Date":  datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Score": wellbeing_score,
        "Confidence": round(confidence, 2),
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

    update_streak()