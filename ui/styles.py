"""Custom CSS styles for the Streamlit steganography app."""


def get_custom_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
.stApp {
    font-family: 'Inter', sans-serif;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
}
section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #6dd5ed, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}
.hero-banner p { color: #b0b0c0; font-size: 1.05rem; }

/* ── Cards ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(167,139,250,0.15);
}
.glass-card h3 {
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #6dd5ed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.glass-card p { color: #b0b0c0; font-size: 0.95rem; }

/* ── Status badges ── */
.status-badge {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
}
.badge-success {
    background: rgba(34,197,94,0.15);
    color: #22c55e;
    border: 1px solid rgba(34,197,94,0.3);
}
.badge-info {
    background: rgba(59,130,246,0.15);
    color: #60a5fa;
    border: 1px solid rgba(59,130,246,0.3);
}
.badge-warn {
    background: rgba(234,179,8,0.15);
    color: #eab308;
    border: 1px solid rgba(234,179,8,0.3);
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin: 1rem 0; }
.metric-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-card .value {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #6dd5ed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card .label { color: #888; font-size: 0.8rem; margin-top: 0.2rem; }

/* ── Encode/Decode tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #302b63, #24243e) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(124,58,237,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.45) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(167,139,250,0.3) !important;
    border-radius: 12px;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(167,139,250,0.6) !important;
}

/* ── Divider ── */
.fancy-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
    margin: 1.5rem 0;
    border: none;
}

/* ── Workflow steps ── */
.workflow-step {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.5rem 0;
}
.step-num {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #a78bfa);
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-size: 0.75rem; font-weight: 700;
    flex-shrink: 0;
}
.step-text { color: #c0c0d0; font-size: 0.9rem; }
</style>
"""
