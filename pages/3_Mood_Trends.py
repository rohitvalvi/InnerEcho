import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os
from modules.theme import theme

st.markdown(theme(), unsafe_allow_html=True)


MOOD_FILE = "data/mood_log.json"
os.makedirs("data", exist_ok=True)

MOOD_COLORS = {
    "Joy":      "#FFD700",
    "Sadness":  "#6495ED",
    "Fear":     "#9370DB",
    "Anger":    "#FF6347",
    "Love":     "#FF69B4",
    "Surprise": "#FFA500",
    "Neutral":  "#90EE90",
}

WELLBEING_BASE = {
    "joy": 0.90,
    "love": 0.85,
    "surprise": 0.65,
    "neutral": 0.55,
    "anger": 0.30,
    "sadness": 0.25,
    "fear": 0.20,
}


def emotion_to_wellbeing(emotion: str, confidence: float) -> float:
    base = WELLBEING_BASE.get(str(emotion).lower(), 0.50)
    confidence = max(0.0, min(1.0, float(confidence)))
    return round(0.5 + (base - 0.5) * confidence, 2)

@st.cache_data(ttl=1)
def _read_mood_file() -> list:
    if os.path.exists(MOOD_FILE):
        try:
            with open(MOOD_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def load_mood_file() -> list:
    return _read_mood_file()

def save_mood_file(data: list) -> None:
    with open(MOOD_FILE, "w") as f:
        json.dump(data, f, indent=2)
    _read_mood_file.clear()

def delete_mood_file() -> None:
    if os.path.exists(MOOD_FILE):
        os.remove(MOOD_FILE)
    _read_mood_file.clear()

if "mood_cleared" not in st.session_state:
    st.session_state.mood_cleared = False

file_data = load_mood_file()

if st.session_state.mood_cleared:
    st.session_state.mood_data = []
elif file_data:
    st.session_state.mood_data    = file_data
    st.session_state.mood_cleared = False
elif "mood_data" in st.session_state and len(st.session_state.mood_data) > 0:
    save_mood_file(st.session_state.mood_data)
    st.session_state.mood_cleared = False
else:
    st.session_state.mood_data = []

st.header("Your Emotional Journey")
st.caption("Visualize your mood patterns over time.")

if len(st.session_state.mood_data) == 0:
    st.info("No mood data yet.")
    st.info("Start chatting with your Companion to build your mood history.")
    st.stop()

normalized = []
needs_save = False
for entry in st.session_state.mood_data:
    mood = str(entry.get("Mood", "Neutral")).capitalize()
    date_val = entry.get("Date")

    if "Confidence" in entry:
        confidence = max(0.0, min(1.0, float(entry.get("Confidence", 0.5))))
        score = max(0.0, min(1.0, float(entry.get("Score", emotion_to_wellbeing(mood, confidence)))))
    else:
        # Legacy records used Score as model confidence. Convert to well-being score.
        confidence = max(0.0, min(1.0, float(entry.get("Score", 0.5))))
        score = emotion_to_wellbeing(mood, confidence)
        needs_save = True

    normalized.append({
        "Date": date_val,
        "Mood": mood,
        "Score": round(score, 2),
        "Confidence": round(confidence, 2),
    })

if needs_save:
    st.session_state.mood_data = normalized
    save_mood_file(normalized)

df = pd.DataFrame(normalized)
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# ── Summary metrics ───────────────────────────────────────────────────────────
st.subheader("Summary")

latest_mood  = df.iloc[-1]["Mood"]
latest_score = df.iloc[-1]["Score"]
avg_score    = df["Score"].mean()
best_mood    = df.loc[df["Score"].idxmax(), "Mood"]

if len(df) >= 2:
    recent_avg   = df.tail(7)["Score"].mean()
    previous_avg = df.iloc[:-7]["Score"].mean() if len(df) > 7 else df.iloc[0]["Score"]
    delta_val    = round((recent_avg - previous_avg) * 100, 1)
    delta_str    = f"{'+' if delta_val >= 0 else ''}{delta_val}%"
else:
    delta_str = None

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Mood",       latest_mood,                  delta=delta_str)
col2.metric("Latest Score",       f"{int(latest_score * 100)}%")
col3.metric("Average Well-being", f"{int(avg_score * 100)}%")
col4.metric("Best Mood Recorded", best_mood)

st.divider()

# ── Line chart ────────────────────────────────────────────────────────────────
st.subheader("Well-being Over Time")

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=df["Date"], y=df["Score"],
    mode="lines",
    line=dict(color="#00d4ff", width=2),
    showlegend=False,
    hoverinfo="skip",
))
for mood, color in MOOD_COLORS.items():
    subset = df[df["Mood"] == mood]
    if subset.empty:
        continue
    fig_line.add_trace(go.Scatter(
        x=subset["Date"], y=subset["Score"],
        mode="markers", name=mood,
        marker=dict(color=color, size=12, line=dict(width=1, color="white")),
        hovertemplate=f"<b>%{{x|%Y-%m-%d %H:%M}}</b><br>Mood: {mood}<br>Score: %{{y:.0%}}<extra></extra>",
    ))
fig_line.update_layout(
    title="Emotional Score Over Time",
    yaxis=dict(tickformat=".0%", range=[0, 1.05]),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    legend_title="Mood", hovermode="x unified",
)
st.plotly_chart(fig_line, use_container_width=True)

# ── Bar chart ─────────────────────────────────────────────────────────────────
st.subheader("Average Score by Mood")

avg_by_mood = (
    df.groupby("Mood")["Score"].mean().reset_index()
    .rename(columns={"Score": "Avg Score"})
    .sort_values("Avg Score", ascending=False)
)
fig_bar = px.bar(
    avg_by_mood, x="Mood", y="Avg Score",
    color="Mood", color_discrete_map=MOOD_COLORS,
    title="Average Well-being Score per Mood",
    text=avg_by_mood["Avg Score"].apply(lambda x: f"{int(x * 100)}%"),
)
fig_bar.update_layout(
    yaxis=dict(tickformat=".0%", range=[0, 1.05]),
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
)
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

# ── Pie chart ─────────────────────────────────────────────────────────────────
st.subheader("Mood Distribution")

mood_counts = df["Mood"].value_counts().reset_index()
mood_counts.columns = ["Mood", "Count"]
fig_pie = px.pie(
    mood_counts, values="Count", names="Mood",
    color="Mood", color_discrete_map=MOOD_COLORS,
    title="Distribution of Moods Recorded", hole=0.4,
)
fig_pie.update_traces(
    textposition="inside", textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
)
st.plotly_chart(fig_pie, use_container_width=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
with st.expander("View Raw Mood Data"):
    display_df = df[["Date", "Mood", "Score"]].copy()
    display_df["Score"] = display_df["Score"].apply(lambda x: f"{int(x * 100)}%")
    display_df["Date"]  = display_df["Date"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(display_df.iloc[::-1].reset_index(drop=True), use_container_width=True)

st.divider()
col_clr, _ = st.columns([1, 4])
with col_clr:
    if st.button("Clear All Mood Data", use_container_width=True, type="primary"):
        st.session_state.mood_cleared = True
        st.session_state.mood_data    = []
        delete_mood_file()
        st.rerun()