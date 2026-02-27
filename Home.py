import streamlit as st

st.set_page_config(
    page_title="InnerEcho — Mental Health Companion",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    from modules.theme import theme
    st.markdown(theme(), unsafe_allow_html=True)
except Exception:
    pass

st.markdown("""
<style>
/* Hide only menu and footer — NEVER hide header/toolbar (breaks sidebar toggle) */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* Keep header transparent — do NOT set display:none */
header[data-testid="stHeader"] {
    background:     transparent !important;
    pointer-events: auto !important;
}

/* Sidebar toggle button — always visible and styled */
[data-testid="collapsedControl"] {
    visibility:     visible !important;
    display:        flex !important;
    opacity:        1 !important;
    pointer-events: all !important;
    z-index:        999999 !important;
    position:       fixed !important;
    top:            0.5rem !important;
    left:           0.5rem !important;
}

[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
    background:      rgba(14,24,50,0.9) !important;
    border:          1px solid rgba(255,255,255,0.15) !important;
    border-radius:   10px !important;
    color:           rgba(255,255,255,0.85) !important;
    visibility:      visible !important;
    display:         flex !important;
    opacity:         1 !important;
    pointer-events:  all !important;
    backdrop-filter: blur(12px) !important;
    transition:      all 0.2s ease !important;
}

[data-testid="collapsedControl"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
    background:   rgba(14,165,233,0.25) !important;
    border-color: rgba(14,165,233,0.6)  !important;
}

.block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    streak = st.session_state.streak
    st.markdown(f"""
        <div style='background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(14,165,233,0.2));
            border:1px solid rgba(255,255,255,0.1);border-radius:12px;
            padding:14px 16px;text-align:center;'>
            <div style='font-size:1.5rem'>&#128293;</div>
            <div style='font-size:1.4rem;font-weight:600;color:#f0c060'>{streak}</div>
            <div style='font-size:0.75rem;color:rgba(255,255,255,0.5);
                letter-spacing:0.08em;text-transform:uppercase'>Day Streak</div>
        </div>
    """, unsafe_allow_html=True)

# ── Page content ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

.mb-hero{text-align:center;padding:2.5rem 1rem 1.5rem;animation:mbFadeUp .8s ease both}
.mb-hero .eyebrow{font-size:.75rem;letter-spacing:.25em;text-transform:uppercase;color:#0ea5e9;margin-bottom:.8rem;font-family:'DM Sans',sans-serif}
.mb-hero h1{font-family:'Cormorant Garamond',serif!important;font-size:clamp(2.6rem,6vw,4.8rem)!important;font-weight:300!important;line-height:1.1!important;background:linear-gradient(135deg,#ffffff 0%,#a78bfa 45%,#0ea5e9 100%);-webkit-background-clip:text!important;-webkit-text-fill-color:transparent!important;background-clip:text!important;margin-bottom:1rem!important}
.mb-hero .sub{font-size:1.05rem;color:rgba(255,255,255,.55);max-width:520px;margin:0 auto 2rem;font-family:'DM Sans',sans-serif;line-height:1.7}
.mb-scene-wrap{position:relative;max-width:860px;margin:0 auto 3.5rem}
.mb-scene{perspective:1400px;width:100%}
.mb-dashboard{transform:rotateX(12deg) rotateY(-4deg) rotateZ(1deg);transform-style:preserve-3d;transition:transform .6s cubic-bezier(.34,1.56,.64,1);border-radius:20px;overflow:hidden;box-shadow:0 60px 120px rgba(0,0,0,.7),0 20px 60px rgba(14,165,233,.15),0 0 0 1px rgba(255,255,255,.08)}
.mb-scene:hover .mb-dashboard{transform:rotateX(4deg) rotateY(-1deg) rotateZ(0)}
.mb-db-chrome{background:rgba(17,24,39,.98);border-bottom:1px solid rgba(255,255,255,.08);padding:10px 16px;display:flex;align-items:center;gap:8px}
.mb-dot{width:10px;height:10px;border-radius:50%}
.mb-dot-r{background:#ff5f57}.mb-dot-y{background:#febc2e}.mb-dot-g{background:#28c840}
.mb-db-title{font-size:.72rem;color:rgba(255,255,255,.35);margin-left:auto;margin-right:auto;font-family:'DM Sans',sans-serif;letter-spacing:.08em}
.mb-db-body{background:linear-gradient(160deg,#0b0f24 0%,#0f1629 100%);display:grid;grid-template-columns:170px 1fr;min-height:360px}
.mb-db-sidebar{background:rgba(7,8,15,.9);border-right:1px solid rgba(255,255,255,.06);padding:18px 10px;display:flex;flex-direction:column;gap:5px}
.mb-nav-logo{font-family:'Cormorant Garamond',serif;font-size:.95rem;color:rgba(255,255,255,.8);padding:0 8px 12px;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:6px}
.mb-nav-item{padding:7px 11px;border-radius:7px;font-size:.7rem;font-family:'DM Sans',sans-serif;color:rgba(255,255,255,.4);display:flex;align-items:center;gap:7px}
.mb-nav-item.active{background:rgba(14,165,233,.12);color:#0ea5e9;border-left:2px solid #0ea5e9}
.mb-db-content{padding:18px 20px;display:flex;flex-direction:column;gap:12px}
.mb-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.mb-metric{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:9px;padding:11px 13px}
.mb-metric-val{font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:white;line-height:1;margin-bottom:3px}
.mb-metric-lbl{font-size:.6rem;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:.1em;font-family:'DM Sans',sans-serif}
.mb-chart-area{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:9px;padding:11px 13px;height:100px;overflow:hidden}
.mb-chart-label{font-size:.62rem;color:rgba(255,255,255,.4);font-family:'DM Sans',sans-serif;letter-spacing:.07em;text-transform:uppercase;margin-bottom:6px}
.mb-sparkline{width:100%;height:62px}
.mb-chat-area{display:flex;flex-direction:column;gap:6px}
.mb-bubble{padding:7px 11px;border-radius:8px;font-size:.67rem;font-family:'DM Sans',sans-serif;line-height:1.4;max-width:85%}
.mb-bubble-user{background:rgba(14,165,233,.1);border:1px solid rgba(14,165,233,.2);color:rgba(255,255,255,.75);align-self:flex-end;border-bottom-right-radius:2px}
.mb-bubble-ai{background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.2);color:rgba(255,255,255,.65);border-bottom-left-radius:2px}
.mb-typing{display:flex;gap:4px;align-items:center;padding:8px 11px}
.mb-typing span{width:5px;height:5px;border-radius:50%;background:#a78bfa;animation:mbTyping 1.2s ease infinite}
.mb-typing span:nth-child(2){animation-delay:.2s}
.mb-typing span:nth-child(3){animation-delay:.4s}
@keyframes mbTyping{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-5px);opacity:1}}
.mb-badge{position:absolute;background:rgba(14,24,50,.92);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:7px 13px;font-family:'DM Sans',sans-serif;font-size:.7rem;color:rgba(255,255,255,.8);backdrop-filter:blur(12px);box-shadow:0 8px 30px rgba(0,0,0,.4);display:flex;align-items:center;gap:7px;white-space:nowrap;animation:mbFloat 4s ease-in-out infinite;z-index:10}
.mb-badge-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.mb-badge-1{top:-16px;left:-10px;animation-delay:0s}
.mb-badge-2{top:28%;right:-20px;animation-delay:1.2s}
.mb-badge-3{bottom:-14px;left:10%;animation-delay:2.4s}
@keyframes mbFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.mb-features{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:0 0 2rem;animation:mbFadeUp .9s ease .5s both}
.mb-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:22px 18px;transition:all .3s cubic-bezier(.34,1.56,.64,1);position:relative;overflow:hidden;cursor:default}
.mb-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--ca,linear-gradient(90deg,#7c3aed,#0ea5e9));opacity:0;transition:opacity .3s ease}
.mb-card:hover::before{opacity:1}
.mb-card:hover{transform:translateY(-6px);border-color:rgba(255,255,255,.14);box-shadow:0 20px 50px rgba(0,0,0,.4)}
.mb-card-icon{font-size:1.6rem;margin-bottom:11px;display:block}
.mb-card-title{font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:rgba(255,255,255,.9);margin-bottom:7px;font-weight:400}
.mb-card-desc{font-size:.78rem;color:rgba(255,255,255,.42);line-height:1.65;font-family:'DM Sans',sans-serif}
.mb-card-tag{display:inline-block;margin-top:13px;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;padding:3px 10px;border-radius:20px;font-family:'DM Sans',sans-serif}
.mb-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,.06);border-radius:16px;overflow:hidden;margin-bottom:2rem;animation:mbFadeUp 1s ease .7s both}
.mb-stat{background:rgba(7,8,15,.8);padding:20px 28px;text-align:center}
.mb-stat-num{font-family:'Cormorant Garamond',serif;font-size:2.1rem;font-weight:300;background:linear-gradient(135deg,#a78bfa,#0ea5e9);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.mb-stat-lbl{font-size:.72rem;color:rgba(255,255,255,.4);font-family:'DM Sans',sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-top:4px}
.mb-disclaimer{text-align:center;font-size:.74rem;color:rgba(255,255,255,.25);font-family:'DM Sans',sans-serif;padding:1rem 0 .5rem;border-top:1px solid rgba(255,255,255,.05);line-height:1.6}
@keyframes mbFadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
</style>

<div class="mb-hero">
    <div class="eyebrow">AI-Powered Mental Wellness</div>
    <h1>Welcome to InnerEcho</h1>
    <p class="sub">Your empathetic companion for emotional well-being — always available, always non-judgmental.</p>
</div>

<div class="mb-scene-wrap">
    <div class="mb-badge mb-badge-1"><div class="mb-badge-dot" style="background:#10b981"></div>AI Companion Active</div>
    <div class="mb-badge mb-badge-2"><div class="mb-badge-dot" style="background:#f0c060"></div>Mood: 78% Positive</div>
    <div class="mb-badge mb-badge-3"><div class="mb-badge-dot" style="background:#a78bfa"></div>End-to-End Secure</div>
    <div class="mb-scene">
        <div class="mb-dashboard">
            <div class="mb-db-chrome">
                <div class="mb-dot mb-dot-r"></div><div class="mb-dot mb-dot-y"></div><div class="mb-dot mb-dot-g"></div>
                <span class="mb-db-title">innerecho.app</span>
            </div>
            <div class="mb-db-body">
                <div class="mb-db-sidebar">
                    <div class="mb-nav-logo">InnerEcho</div>
                    <div class="mb-nav-item active">Companion Chat</div>
                    <div class="mb-nav-item">Personal Diary</div>
                    <div class="mb-nav-item">Mood Trends</div>
                    <div class="mb-nav-item">Emergency</div>
                </div>
                <div class="mb-db-content">
                    <div class="mb-metrics">
                        <div class="mb-metric"><div class="mb-metric-val" style="color:#f0c060">Joy</div><div class="mb-metric-lbl">Current Mood</div></div>
                        <div class="mb-metric"><div class="mb-metric-val">78%</div><div class="mb-metric-lbl">Well-being Score</div></div>
                        <div class="mb-metric"><div class="mb-metric-val" style="color:#10b981">+12%</div><div class="mb-metric-lbl">Weekly Trend</div></div>
                    </div>
                    <div class="mb-chart-area">
                        <div class="mb-chart-label">Well-being Over Time</div>
                        <svg class="mb-sparkline" viewBox="0 0 400 60" preserveAspectRatio="none">
                            <defs><linearGradient id="lg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0ea5e9" stop-opacity="0.4"/><stop offset="100%" stop-color="#0ea5e9" stop-opacity="0"/></linearGradient></defs>
                            <path d="M0,45 C30,40 60,20 100,25 C140,30 160,42 200,30 C240,18 280,10 320,15 C360,20 380,8 400,5 L400,60 L0,60 Z" fill="url(#lg1)"/>
                            <path d="M0,45 C30,40 60,20 100,25 C140,30 160,42 200,30 C240,18 280,10 320,15 C360,20 380,8 400,5" fill="none" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round"/>
                            <circle cx="100" cy="25" r="3.5" fill="#0ea5e9"/>
                            <circle cx="200" cy="30" r="3.5" fill="#a78bfa"/>
                            <circle cx="400" cy="5" r="4" fill="#f0c060" stroke="white" stroke-width="1.5"/>
                        </svg>
                    </div>
                    <div class="mb-chat-area">
                        <div class="mb-bubble mb-bubble-user">I've been feeling overwhelmed lately...</div>
                        <div class="mb-bubble mb-bubble-ai">I hear you. It's okay to feel that way. Would you like to talk about what's been on your mind?</div>
                        <div class="mb-typing"><span></span><span></span><span></span></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="mb-features">
    <div class="mb-card" style="--ca:linear-gradient(90deg,#7c3aed,#0ea5e9)">
        <span class="mb-card-icon">&#128172;</span>
        <div class="mb-card-title">Companion Chat</div>
        <div class="mb-card-desc">An empathetic AI that detects your emotional state and responds with genuine care — 24/7, judgment-free.</div>
        <span class="mb-card-tag" style="background:rgba(124,58,237,0.15);color:#a78bfa">AI Powered</span>
    </div>
    <div class="mb-card" style="--ca:linear-gradient(90deg,#0ea5e9,#10b981)">
        <span class="mb-card-icon">&#128214;</span>
        <div class="mb-card-title">Personal Diary</div>
        <div class="mb-card-desc">Password-protected private space to record thoughts, tag moods, search entries, and reflect over time.</div>
        <span class="mb-card-tag" style="background:rgba(16,185,129,0.12);color:#10b981">Encrypted</span>
    </div>
    <div class="mb-card" style="--ca:linear-gradient(90deg,#f0c060,#f97316)">
        <span class="mb-card-icon">&#128202;</span>
        <div class="mb-card-title">Mood Trends</div>
        <div class="mb-card-desc">Interactive charts showing your emotional journey — line trends, mood distribution, and weekly well-being scores.</div>
        <span class="mb-card-tag" style="background:rgba(240,192,96,0.12);color:#f0c060">Live Charts</span>
    </div>
    <div class="mb-card" style="--ca:linear-gradient(90deg,#ef4444,#f97316)">
        <span class="mb-card-icon">&#128680;</span>
        <div class="mb-card-title">Emergency Support</div>
        <div class="mb-card-desc">Instant access to crisis helplines, guardian alerts, and grounding exercises — when it matters most.</div>
        <span class="mb-card-tag" style="background:rgba(239,68,68,0.12);color:#ef4444">Always Ready</span>
    </div>
</div>

<div class="mb-stats">
    <div class="mb-stat"><div class="mb-stat-num">6</div><div class="mb-stat-lbl">Emotions Detected</div></div>
    <div class="mb-stat"><div class="mb-stat-num">24/7</div><div class="mb-stat-lbl">Always Available</div></div>
    <div class="mb-stat"><div class="mb-stat-num">100%</div><div class="mb-stat-lbl">Private & Secure</div></div>
</div>

<div class="mb-disclaimer">
    InnerEcho is an AI-powered support tool and is <strong>NOT</strong> a substitute for clinical diagnosis,
    therapy, or emergency medical intervention. Always seek professional help when needed.
</div>
""", unsafe_allow_html=True)