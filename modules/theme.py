def theme():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --midnight:      #07080f;
        --deep-navy:     #0b0f24;
        --glass-bg:      rgba(255,255,255,0.04);
        --glass-border:  rgba(255,255,255,0.09);
        --teal:          #0ea5e9;
        --teal-glow:     rgba(14,165,233,0.25);
        --lavender:      #a78bfa;
        --gold:          #f0c060;
        --text-primary:  rgba(255,255,255,0.92);
        --text-secondary:rgba(255,255,255,0.55);
        --radius-sm:     10px;
        --radius-md:     16px;
        --shadow-glow:   0 0 40px rgba(14,165,233,0.12), 0 8px 32px rgba(0,0,0,0.4);
    }

    html, body, [class*="css"], .stApp {
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text-primary) !important;
    }

    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 300 !important;
        letter-spacing: 0.02em !important;
    }

    /* Animated aurora background */
    [data-testid="stAppViewContainer"] {
        background: var(--midnight) !important;
        position: relative !important;
        overflow: visible !important;
        display: flex !important;
        flex-direction: row !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: -30%; left: -20%;
        width: 80vw; height: 80vh;
        background: radial-gradient(ellipse, rgba(99,57,185,0.18) 0%, transparent 65%);
        animation: aurora1 18s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        bottom: -20%; right: -15%;
        width: 70vw; height: 70vh;
        background: radial-gradient(ellipse, rgba(14,165,233,0.14) 0%, transparent 65%);
        animation: aurora2 22s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes aurora1 {
        0%   { transform: translate(0,0)    scale(1);    opacity: 0.7; }
        50%  { transform: translate(8%,5%)  scale(1.05); opacity: 1;   }
        100% { transform: translate(5%,-5%) scale(1.08); opacity: 1;   }
    }
    @keyframes aurora2 {
        0%   { transform: translate(0,0)    scale(1);   opacity: 0.6; }
        50%  { transform: translate(-8%,-5%)scale(1.1); opacity: 1;   }
        100% { transform: translate(5%,8%)  scale(0.92);opacity: 0.7; }
    }

    [data-testid="stMain"] { background: transparent !important; position: relative; z-index: 1; }
    .main .block-container { background: transparent !important; padding: 2.5rem 3rem !important; max-width: 1100px !important; }

    /* Sidebar wrapper container */
    [data-testid="stSidebarContent"] {
        display: flex !important;
        visibility: visible !important;
        flex-direction: column !important;
    }
    
    /* Ensure sidebar parent layout */
    .st-emotion-cache-1r6df1c {
        display: flex !important;
        flex-direction: row !important;
    }

    /* Sidebar - Always Visible */
    [data-testid="stSidebar"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
        height: 100vh !important;
        background: linear-gradient(180deg, rgba(15,8,40,0.97) 0%, rgba(7,8,15,0.98) 100%) !important;
        border-right: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 4px 0 40px rgba(0,0,0,0.5) !important;
        position: relative !important;
        z-index: 100 !important;
        pointer-events: auto !important;
        flex-direction: column !important;
        overflow-y: auto !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--lavender), var(--teal), var(--gold));
        opacity: 0.8;
    }

    /* Sidebar content area */
    [data-testid="stSidebar"] > div {
        display: flex !important;
        visibility: visible !important;
        flex-direction: column !important;
    }

    /* Page titles */
    .stApp h1 {
        font-size: 2.6rem !important;
        background: linear-gradient(135deg, #ffffff 0%, var(--teal) 50%, var(--lavender) 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        animation: fadeSlideDown 0.7s ease both;
    }
    .stApp h2 { font-size: 1.6rem !important; color: rgba(255,255,255,0.85) !important; }
    .stApp h3 { font-size: 1.15rem !important; color: rgba(255,255,255,0.7) !important; }

    @keyframes fadeSlideDown {
        from { opacity: 0; transform: translateY(-14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .stApp .stCaption p { color: var(--text-secondary) !important; font-size: 0.88rem !important; }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        padding: 20px 22px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: var(--shadow-glow) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        animation: fadeUp 0.6s ease both;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 0 50px var(--teal-glow), 0 12px 40px rgba(0,0,0,0.5) !important;
        border-color: rgba(14,165,233,0.3) !important;
    }
    [data-testid="stMetricValue"] { color: white !important; font-family: 'Cormorant Garamond', serif !important; font-size: 2rem !important; font-weight: 300 !important; }
    [data-testid="stMetricLabel"] { color: var(--text-secondary) !important; font-size: 0.78rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }

    .stColumn:nth-child(1) [data-testid="stMetric"] { animation-delay: 0.05s; }
    .stColumn:nth-child(2) [data-testid="stMetric"] { animation-delay: 0.15s; }
    .stColumn:nth-child(3) [data-testid="stMetric"] { animation-delay: 0.25s; }
    .stColumn:nth-child(4) [data-testid="stMetric"] { animation-delay: 0.35s; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #0ea5e9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.04em !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1) !important;
        box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 8px 30px rgba(124,58,237,0.45) !important;
    }
    .stButton > button:active { transform: translateY(0) scale(0.98) !important; }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 3px var(--teal-glow) !important;
        outline: none !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        backdrop-filter: blur(10px) !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.75rem !important;
        animation: fadeUp 0.4s ease both !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: background 0.2s ease !important;
    }
    .streamlit-expanderHeader:hover { background: rgba(255,255,255,0.07) !important; }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid var(--glass-border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--radius-sm) var(--radius-sm) !important;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: var(--radius-sm) !important;
        backdrop-filter: blur(8px) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Plotly charts */
    [data-testid="stPlotlyChart"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        padding: 0.5rem !important;
        box-shadow: var(--shadow-glow) !important;
        animation: fadeUp 0.7s ease both;
    }

    /* Dividers */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent 0%, rgba(14,165,233,0.4) 30%, rgba(167,139,250,0.4) 70%, transparent 100%) !important;
        margin: 1.5rem 0 !important;
    }

    /* Sidebar nav */
    [data-testid="stSidebarNav"] {
        display: flex !important;
        visibility: visible !important;
        flex-direction: column !important;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: var(--radius-sm) !important;
        transition: background 0.2s ease, padding-left 0.2s ease !important;
        color: var(--text-secondary) !important;
    }
    [data-testid="stSidebarNav"] a:hover,
    [data-testid="stSidebarNav"] a[aria-selected="true"] {
        background: rgba(14,165,233,0.1) !important;
        color: var(--text-primary) !important;
        padding-left: 1.2rem !important;
        border-left: 2px solid var(--teal) !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-md) !important;
        background: var(--glass-bg) !important;
    }

    /* Toast */
    [data-testid="stToast"] {
        background: rgba(15,23,42,0.9) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-sm) !important;
        backdrop-filter: blur(16px) !important;
    }

    /* Link buttons */
    .stLinkButton > a {
        background: transparent !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--teal) !important;
        border-radius: var(--radius-sm) !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.25s ease !important;
    }
    .stLinkButton > a:hover {
        background: var(--teal-glow) !important;
        border-color: var(--teal) !important;
        transform: translateY(-2px) !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--lavender), var(--teal)); border-radius: 10px; }

    ::selection { background: var(--teal-glow); color: white; }

    /* Noise texture overlay */
    body::after {
        content: '';
        position: fixed; inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='1'/%3E%3C/svg%3E");
        opacity: 0.025;
        pointer-events: none;
        z-index: 9999;
    }

    /* ── Sidebar: Always visible - Disable closing button ─────── */
    /* Hide the native collapse button */
    [data-testid="collapsedControl"] {
        display:        none !important;
        visibility:     hidden !important;
        pointer-events: none !important;
    }
    /* Hide the custom toggle button */
    #ie-sidebar-btn {
        display:         none !important;
        visibility:      hidden !important;
        pointer-events:  none !important;
    }
    #ie-sidebar-btn:hover {
        background:   rgba(14,165,233,0.25);
        border-color: rgba(14,165,233,0.6);
        box-shadow:   0 4px 24px rgba(14,165,233,0.3);
    }
    #ie-sidebar-btn svg {
        width: 18px; height: 18px;
        fill: none; stroke: rgba(255,255,255,0.85);
        stroke-width: 2; stroke-linecap: round;
    }
    </style>

    <script>
    (function() {
        function setupSidebar() {
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                // Force sidebar to always be visible
                sidebar.style.display = 'flex';
                sidebar.style.visibility = 'visible';
                sidebar.style.opacity = '1';
            }
            
            // Hide all collapse/toggle buttons
            const collapseBtn = document.querySelector('[data-testid="collapsedControl"]');
            if (collapseBtn) collapseBtn.style.display = 'none';
            
            const toggleBtn = document.getElementById('ie-sidebar-btn');
            if (toggleBtn) toggleBtn.style.display = 'none';
        }

        setupSidebar();
        setTimeout(setupSidebar, 600);
        setTimeout(setupSidebar, 1800);
        
        // Watch for any changes and keep sidebar visible
        new MutationObserver(setupSidebar).observe(document.body, {
            attributes: true,
            childList: true,
            subtree: true
        });
    })();
    </script>
    """