# InnerEcho
AI Mental Health Companion

InnerEcho is an AI-powered mental health companion web app built with Streamlit. It detects your emotions in real time, responds with empathy, tracks your mood over time, and provides immediate access to crisis resources — all in a secure, private environment.

Features
Companion Chat

Real-time emotion detection using distilbert-base-uncased-emotion
Context-aware AI responses powered by Meta-Llama-3-8B-Instruct
Crisis keyword detection with instant helpline resources
Daily check-in streak tracker
Full conversation history within session

Personal Diary

Password-protected with SHA-256 hashed authentication
Create, search, and delete diary entries
Mood tagging for each entry
Password reset and change functionality
Data persisted locally to data/diary_entries.json

Mood Trends

Interactive line chart — well-being score over time
Bar chart — average score per mood type
Donut chart — mood distribution
KPI metrics — current mood, latest score, weekly trend delta
Demo data shown until real data is generated

Emergency Support

Crisis helplines (iCall, Vandrevala Foundation, Snehi)
Guardian SOS alert system
5-4-3-2-1 grounding technique
Links to professional resources

Profile

Personal details — name, age, gender, pronouns, bio
Profile photo upload
Mental health goals with progress tracking
Emergency contacts management
Interests and hobbies — music, movies, activities


Tech Stack
LayerTechnologyFrontendStreamlit, HTML/CSS, Plotly
AI — Emotion Detectionbhadresh-savani/distilbert-base-uncased-emotion
AI — Chatmeta-llama/Meta-Llama-3-8B-Instruct
AI APIHuggingFace Inference API
Data StorageJSON files (local)
AuthSHA-256 password hashing
FontsCormorant Garamond, DM Sans

innerecho/
├── Home.py                      # Landing page with 3D dashboard preview
├── requirements.txt             # Python dependencies
├── .gitignore                   # Excludes secrets and data files
│
├── modules/
│   ├── __init__.py
│   ├── ai_engine.py             # Emotion detection, AI responses, mood saving
│   └── theme.py                 # Global CSS theme (dark luxury design)
│
├── pages/
│   ├── 1_Companion_Chat.py      # AI chat interface
│   ├── 2_Personal_Diary.py      # Password-protected diary
│   ├── 3_Mood_Trends.py         # Mood visualization dashboard
│   ├── 4_Emergency.py           # Crisis support page
│   └── _Profile.py              # User profile page
│
├── assets/
│   └── logo.svg                 # InnerEcho logo
│
├── data/                        # Auto-created on first run (gitignored)
│   ├── auth.json                # Hashed diary password
│   ├── diary_entries.json       # Diary entries
│   ├── mood_log.json            # Mood history
│   └── profile.json             # User profile data
│
└── .streamlit/
    └── secrets.toml             # HuggingFace API token (gitignored)


    AI Models
ModelPurposebhadresh-savani/distilbert-base-uncased-emotion  : Detects emotion in user messages
meta-llama/Meta-Llama-3-8B-Instruct: Generates empathetic chat responses

Data & Privacy

All user data is stored locally in the data/ folder
Diary entries are protected by a SHA-256 hashed password
No data is sent to any external server except HuggingFace for AI inference
The data/ folder is excluded from Git via .gitignore


Disclaimer

InnerEcho is an AI-powered support tool and is NOT a substitute for clinical diagnosis, therapy, or emergency medical intervention. If you are in crisis, please contact a professional immediately.
India Crisis Helplines:




Author
Built with care by Rohit Valvi

"Sometimes the bravest thing you can do is ask for help."
