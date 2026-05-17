import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
import os

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Win Probability Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS  –  Cricket-themed dark design
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: #0a0e1a;
    color: #e8ecf4;
}

/* ── Main container ── */
.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1200px;
}

/* ── Hero title ── */
.hero-title {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 40%, #ff6b6b 80%, #ee0979 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.1;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

.hero-sub {
    text-align: center;
    color: #8892aa;
    font-size: 1.05rem;
    font-weight: 400;
    margin-bottom: 2rem;
}

/* ── Divider ── */
hr.custom-hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #f7971e, #ffd200, transparent);
    margin: 1.5rem 0;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, #141928 0%, #1c2338 100%);
    border: 1px solid #2a3352;
    border-radius: 18px;
    padding: 1.6rem 1.4rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f7971e, #ffd200);
    border-radius: 18px 18px 0 0;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(247,151,30,0.18);
}
.metric-card h2 {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
    line-height: 1;
}
.metric-card p {
    margin: 0.4rem 0 0;
    color: #8892aa;
    font-size: 0.88rem;
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Win card ── */
.win-card h2  { color: #36d399; }
.win-card::before { background: linear-gradient(90deg, #36d399, #3abf8f); }

/* ── Loss card ── */
.loss-card h2 { color: #ff6b6b; }
.loss-card::before { background: linear-gradient(90deg, #ff6b6b, #ee0979); }

/* ── Summary box ── */
.summary-box {
    background: linear-gradient(135deg, #141928 0%, #1c2338 100%);
    border: 1px solid #2a3352;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.2rem;
    line-height: 1.8;
    font-size: 0.97rem;
    color: #c8d0e0;
}
.summary-box h4 {
    color: #ffd200;
    font-size: 1rem;
    margin: 0 0 0.8rem;
    letter-spacing: 0.5px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid #1e2a40;
}
[data-testid="stSidebar"] .sidebar-logo {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.2rem;
}
[data-testid="stSidebar"] h2 {
    color: #ffd200;
    font-size: 1.2rem;
    font-weight: 700;
    text-align: center;
}
[data-testid="stSidebar"] label {
    color: #aab4cc !important;
    font-weight: 500;
    font-size: 0.88rem;
}
[data-testid="stSidebar"] .stSelectbox > div,
[data-testid="stSidebar"] .stNumberInput > div {
    border-radius: 10px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #f7971e, #ffd200) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.5px;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px rgba(247,151,30,0.35) !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
}

/* ── Info tag ── */
.info-tag {
    background: rgba(247,151,30,0.12);
    color: #ffd200;
    border: 1px solid rgba(247,151,30,0.3);
    border-radius: 8px;
    padding: 0.35rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-top: 0.5rem;
}

/* ── Section header ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffd200;
    margin: 1.6rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Progress bar wrapper ── */
.prog-wrap {
    background: #141928;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.8rem;
    border: 1px solid #2a3352;
}
.prog-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.prog-track {
    background: #1e2a40;
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
}
.prog-fill-win {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #36d399, #3abf8f);
    transition: width 1s cubic-bezier(.4,0,.2,1);
}
.prog-fill-loss {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff6b6b, #ee0979);
    transition: width 1s cubic-bezier(.4,0,.2,1);
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────
TEAMS = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Punjab Kings",
    "Kolkata Knight Riders",
    "Mumbai Indians",
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad",
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "pipe.pkl")


# ─────────────────────────────────────────────────────────────
# MODEL LOADER
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


# ─────────────────────────────────────────────────────────────
# PREDICTION LOGIC
# ─────────────────────────────────────────────────────────────
def predict(pipe, batting_team, bowling_team, target, current_score, overs, wickets):
    balls_bowled   = int(overs * 6)
    runs_left      = target - current_score
    balls_left     = 120 - balls_bowled
    wickets_left   = 10 - wickets
    crr            = (current_score * 6) / balls_bowled if balls_bowled > 0 else 0.0
    rrr            = (runs_left * 6) / balls_left       if balls_left  > 0 else 99.99

    input_df = pd.DataFrame({
        "batting_team":  [batting_team],
        "bowling_team":  [bowling_team],
        "runs_left":     [runs_left],
        "balls_left":    [balls_left],
        "wickets_left":  [wickets_left],
        "target":        [target],
        "crr":           [crr],
        "rrr":           [rrr],
    })

    proba        = pipe.predict_proba(input_df)[0]
    win_prob     = round(float(proba[1]) * 100, 2)
    loss_prob    = round(float(proba[0]) * 100, 2)

    return {
        "win_prob":      win_prob,
        "loss_prob":     loss_prob,
        "runs_left":     runs_left,
        "balls_left":    balls_left,
        "wickets_left":  wickets_left,
        "crr":           round(crr, 2),
        "rrr":           round(rrr, 2),
    }


def build_summary(result, batting_team, bowling_team, overs):
    w = result["win_prob"]
    r = result["runs_left"]
    b = result["balls_left"]
    rrr = result["rrr"]
    crr = result["crr"]
    wk  = result["wickets_left"]

    if w >= 75:
        momentum = f"🔥 <b>{batting_team}</b> are in firm control of this chase!"
        assessment = "With plenty of wickets in hand and a healthy run rate, the match is heavily in their favour."
    elif w >= 55:
        momentum = f"⚡ <b>{batting_team}</b> have a slight advantage in this tight contest."
        assessment = f"They need {r} more runs off {b} balls — completely achievable with careful batting."
    elif w >= 45:
        momentum = f"⚖️ This match is perfectly balanced! Either team can win."
        assessment = f"RRR of {rrr:.2f} vs CRR of {crr:.2f} — the next few overs are absolutely crucial."
    elif w >= 25:
        momentum = f"😬 <b>{bowling_team}</b> have their noses in front."
        assessment = f"The required run rate of {rrr:.2f} is demanding with only {wk} wickets left."
    else:
        momentum = f"🏆 <b>{bowling_team}</b> are heavy favourites to win this match!"
        assessment = f"With {r} runs needed off {b} balls, the chase looks almost impossible."

    overs_rem = b // 6
    return (
        f"{momentum}<br><br>"
        f"{assessment}<br><br>"
        f"📊 <b>Snapshot at {overs:.1f} overs:</b> "
        f"CRR <b>{crr:.2f}</b> | RRR <b>{rrr:.2f}</b> | "
        f"Balls remaining <b>{b}</b> | Wickets in hand <b>{wk}</b>"
    )


# ─────────────────────────────────────────────────────────────
# PLOTLY PIE CHART
# ─────────────────────────────────────────────────────────────
def render_pie(batting_team, bowling_team, win_prob, loss_prob):
    fig = go.Figure(
        go.Pie(
            labels=[batting_team, bowling_team],
            values=[win_prob, loss_prob],
            hole=0.52,
            marker=dict(
                colors=["#36d399", "#ff6b6b"],
                line=dict(color="#0a0e1a", width=3),
            ),
            textinfo="label+percent",
            textfont=dict(family="Outfit", size=13, color="#e8ecf4"),
            hovertemplate="%{label}: <b>%{value:.1f}%</b><extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color="#e8ecf4"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.15,
            xanchor="center", x=0.5,
            font=dict(size=12),
        ),
        annotations=[dict(
            text="Win %",
            x=0.5, y=0.5,
            font=dict(size=14, family="Outfit", color="#ffd200"),
            showarrow=False,
        )],
        margin=dict(t=20, b=40, l=20, r=20),
        height=340,
    )
    return fig


# ─────────────────────────────────────────────────────────────
# PLOTLY GAUGE
# ─────────────────────────────────────────────────────────────
def render_gauge(win_prob, batting_team):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=win_prob,
            title=dict(text=f"{batting_team}<br><span style='font-size:0.8em;color:#8892aa'>Win Probability</span>",
                       font=dict(family="Outfit", size=14, color="#e8ecf4")),
            number=dict(suffix="%", font=dict(family="Outfit", size=32, color="#36d399")),
            delta=dict(reference=50, valueformat=".1f"),
            gauge=dict(
                axis=dict(range=[0, 100], tickfont=dict(color="#8892aa")),
                bar=dict(color="#36d399", thickness=0.22),
                bgcolor="#141928",
                borderwidth=0,
                steps=[
                    dict(range=[0,   33], color="#2d1a1a"),
                    dict(range=[33,  67], color="#1a2030"),
                    dict(range=[67, 100], color="#1a2d25"),
                ],
                threshold=dict(
                    line=dict(color="#ffd200", width=4),
                    thickness=0.75,
                    value=50,
                ),
            ),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color="#e8ecf4"),
        margin=dict(t=40, b=20, l=30, r=30),
        height=280,
    )
    return fig


# ─────────────────────────────────────────────────────────────
# ─── SIDEBAR ─────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏏</div>', unsafe_allow_html=True)
    st.markdown("## Match Conditions")
    st.markdown("---")

    batting_team = st.selectbox(
        "🟢 Batting Team (Chasing)",
        TEAMS,
        index=4,
        key="batting_team",
    )
    bowling_team = st.selectbox(
        "🔴 Bowling Team (Defending)",
        [t for t in TEAMS if t != batting_team],
        index=0,
        key="bowling_team",
    )

    st.markdown("---")
    st.markdown("**📊 Match State**")

    target = st.number_input(
        "🎯 Target Score",
        min_value=1, max_value=400, value=180, step=1,
        help="First innings total + 1",
    )
    current_score = st.number_input(
        "🏃 Current Score",
        min_value=0, max_value=400, value=120, step=1,
    )
    overs = st.number_input(
        "⏱️ Overs Completed",
        min_value=0.0, max_value=19.5, value=12.0, step=0.1,
        format="%.1f",
        help="E.g., 12.3 = 12 overs 3 balls",
    )
    wickets = st.number_input(
        "❌ Wickets Fallen",
        min_value=0, max_value=10, value=3, step=1,
    )

    st.markdown("---")
    predict_btn = st.button("⚡ PREDICT WIN PROBABILITY", use_container_width=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;color:#4a5568;font-size:0.75rem;">'
        'Model: Logistic Regression<br>Trained on Kaggle IPL Dataset</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# ─── MAIN PAGE ───────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🏏 IPL Win Probability Predictor</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Real-time run-chase win probability powered by Machine Learning</p>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)

# ── Load model ──────────────────────────────────────────────
pipe = load_model()

if pipe is None:
    st.warning(
        "⚠️  **Model not found.**  \n"
        "Please run the `IPL_Win_Predictor.ipynb` notebook first to train the model "
        "and generate `pipe.pkl`.",
        icon="⚠️",
    )

# ─────────────────────────────────────────────────────────────
# PREDICTION OUTPUT
# ─────────────────────────────────────────────────────────────
if predict_btn:
    if pipe is None:
        st.error("Cannot predict — model file `pipe.pkl` is missing. Run the notebook first.")
    else:
        # Input validation
        balls_bowled = int(overs * 6)
        if balls_bowled == 0:
            st.error("Overs completed must be at least 0.1 (1 ball bowled).")
        elif current_score > target:
            st.error("Current score cannot exceed the target!")
        elif wickets > 10:
            st.error("Wickets fallen cannot exceed 10.")
        else:
            result = predict(pipe, batting_team, bowling_team, target, current_score, overs, wickets)
            win_prob  = result["win_prob"]
            loss_prob = result["loss_prob"]

            # ── Metric cards ─────────────────────────────────
            st.markdown('<div class="section-header">📈 Win Probability</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.markdown(
                    f'<div class="metric-card win-card"><h2>{win_prob:.1f}%</h2>'
                    f'<p>{batting_team}</p><span class="info-tag">🟢 Win Chance</span></div>',
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f'<div class="metric-card loss-card"><h2>{loss_prob:.1f}%</h2>'
                    f'<p>{bowling_team}</p><span class="info-tag" style="background:rgba(255,107,107,0.12);color:#ff6b6b;border-color:rgba(255,107,107,0.3);">🔴 Win Chance</span></div>',
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f'<div class="metric-card"><h2 style="color:#60a5fa;">{result["runs_left"]}</h2>'
                    f'<p>Runs Left</p><span class="info-tag" style="background:rgba(96,165,250,0.12);color:#60a5fa;border-color:rgba(96,165,250,0.3);">🎯 To Win</span></div>',
                    unsafe_allow_html=True,
                )
            with c4:
                st.markdown(
                    f'<div class="metric-card"><h2 style="color:#a78bfa;">{result["balls_left"]}</h2>'
                    f'<p>Balls Left</p><span class="info-tag" style="background:rgba(167,139,250,0.12);color:#a78bfa;border-color:rgba(167,139,250,0.3);">⏱️ Remaining</span></div>',
                    unsafe_allow_html=True,
                )

            # ── Progress bars (HTML) ──────────────────────────
            st.markdown('<div class="section-header">📊 Probability Bars</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="prog-wrap">
                    <div class="prog-label">
                        <span>🟢 {batting_team}</span>
                        <span style="color:#36d399;font-size:1rem;">{win_prob:.1f}%</span>
                    </div>
                    <div class="prog-track">
                        <div class="prog-fill-win" style="width:{win_prob}%;"></div>
                    </div>
                </div>
                <div class="prog-wrap">
                    <div class="prog-label">
                        <span>🔴 {bowling_team}</span>
                        <span style="color:#ff6b6b;font-size:1rem;">{loss_prob:.1f}%</span>
                    </div>
                    <div class="prog-track">
                        <div class="prog-fill-loss" style="width:{loss_prob}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Charts ───────────────────────────────────────
            st.markdown('<div class="section-header">📉 Visual Analysis</div>', unsafe_allow_html=True)
            ch1, ch2 = st.columns([1.1, 1])

            with ch1:
                st.plotly_chart(
                    render_pie(batting_team, bowling_team, win_prob, loss_prob),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )
            with ch2:
                st.plotly_chart(
                    render_gauge(win_prob, batting_team),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

            # ── Run Rate stats ────────────────────────────────
            st.markdown('<div class="section-header">📐 Run Rate Analysis</div>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("Current Run Rate (CRR)", f"{result['crr']:.2f}", help="Runs scored per over so far")
            with r2:
                st.metric("Required Run Rate (RRR)", f"{result['rrr']:.2f}",
                          delta=f"{result['rrr'] - result['crr']:.2f} above CRR",
                          delta_color="inverse")
            with r3:
                st.metric("Wickets in Hand", result["wickets_left"])

            # ── Summary ───────────────────────────────────────
            st.markdown('<div class="section-header">🎙️ Match Analysis</div>', unsafe_allow_html=True)
            summary_html = build_summary(result, batting_team, bowling_team, overs)
            st.markdown(
                f'<div class="summary-box"><h4>📢 MATCH COMMENTARY</h4>{summary_html}</div>',
                unsafe_allow_html=True,
            )

else:
    # ── Default landing state ────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #141928, #1c2338);
            border: 1px dashed #2a3352;
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            margin-top: 2rem;
        ">
            <div style="font-size:5rem;margin-bottom:1rem;">🏏</div>
            <h2 style="color:#ffd200;font-size:1.6rem;font-weight:700;margin:0 0 0.8rem;">
                Ready to Predict?
            </h2>
            <p style="color:#8892aa;font-size:1rem;max-width:480px;margin:0 auto 1.5rem;">
                Fill in the current match conditions in the <b style="color:#ffd200;">sidebar</b>
                and click <b style="color:#36d399;">⚡ PREDICT</b> to see live win probabilities.
            </p>
            <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
                <span style="background:rgba(54,211,153,0.12);color:#36d399;border:1px solid rgba(54,211,153,0.3);border-radius:8px;padding:0.4rem 1rem;font-size:0.85rem;font-weight:600;">📊 Probability Bars</span>
                <span style="background:rgba(247,151,30,0.12);color:#ffd200;border:1px solid rgba(247,151,30,0.3);border-radius:8px;padding:0.4rem 1rem;font-size:0.85rem;font-weight:600;">🥧 Pie Chart</span>
                <span style="background:rgba(96,165,250,0.12);color:#60a5fa;border:1px solid rgba(96,165,250,0.3);border-radius:8px;padding:0.4rem 1rem;font-size:0.85rem;font-weight:600;">🎚️ Gauge Meter</span>
                <span style="background:rgba(167,139,250,0.12);color:#a78bfa;border:1px solid rgba(167,139,250,0.3);border-radius:8px;padding:0.4rem 1rem;font-size:0.85rem;font-weight:600;">🎙️ Commentary</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:#4a5568;font-size:0.8rem;padding-bottom:1rem;">'
    '🏏 IPL Win Probability Predictor &nbsp;|&nbsp; '
    'Logistic Regression · scikit-learn · Streamlit · Plotly'
    '</div>',
    unsafe_allow_html=True,
)
