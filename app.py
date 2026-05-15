import streamlit as st
import pandas as pd
import pickle
import requests
import time

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch – AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# TMDB API  –  replace with your own free key from https://www.themoviedb.org/
# ─────────────────────────────────────────────────────────────────────────────
TMDB_API_KEY = "199636f669ab58f9275caa61c244fdc3"
TMDB_BASE    = "https://api.themoviedb.org/3"
POSTER_BASE  = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER  = "https://placehold.co/300x450/0d0d14/e50914?text=🎬+No+Poster"

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  – cinematic dark theme with film grain & premium typography
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ── Reset & Base ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080810 !important;
}
.main { background-color: #080810 !important; }
.block-container {
    padding: 0 2.5rem 4rem 2.5rem !important;
    max-width: 1400px !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0d14; }
::-webkit-scrollbar-thumb { background: #e50914; border-radius: 3px; }

/* ── Hero / Header ─────────────────────────────────────────────────────── */
.hero-wrapper {
    position: relative;
    background: linear-gradient(135deg, #0d0010 0%, #080810 40%, #0a0005 100%);
    border-bottom: 1px solid #1a1a28;
    padding: 3rem 0 2.2rem 0;
    margin-bottom: 2rem;
    overflow: hidden;
}
.hero-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 10% 50%, rgba(229,9,20,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 40% 60% at 90% 20%, rgba(229,9,20,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(229,9,20,0.15);
    border: 1px solid rgba(229,9,20,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #e50914;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    font-weight: 400;
    color: #fff;
    letter-spacing: 4px;
    line-height: 0.95;
    margin-bottom: 4px;
}
.hero-title span { color: #e50914; }
.hero-tagline {
    font-size: 1.05rem;
    color: #666;
    font-weight: 300;
    letter-spacing: 0.3px;
    margin-top: 10px;
}
.hero-stats {
    display: flex;
    gap: 28px;
    margin-top: 22px;
}
.stat-pill {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: #fff;
    letter-spacing: 1px;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.7rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Divider ───────────────────────────────────────────────────────────── */
.cinema-divider {
    height: 1px;
    background: linear-gradient(90deg, #e50914 0%, #ff4422 30%, transparent 80%);
    border: none;
    margin: 0 0 2rem 0;
    opacity: 0.6;
}

/* ── Section Label ─────────────────────────────────────────────────────── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: #555;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.section-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 24px;
    line-height: 1.2;
}
.section-title span { color: #e50914; }

/* ── Controls ──────────────────────────────────────────────────────────── */
.control-panel {
    background: linear-gradient(135deg, #0e0e1a, #12121f);
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.control-panel::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #e50914, transparent);
}
.stSelectbox > div > div {
    background: #0a0a14 !important;
    border: 1px solid #252535 !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 2px rgba(229,9,20,0.2) !important;
}
.stSelectbox label { color: #888 !important; font-size: 0.78rem !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
.stSlider label { color: #888 !important; font-size: 0.78rem !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
.stSlider > div > div > div { background: #e50914 !important; }
.stSlider > div > div > div > div { background: #1e1e2e !important; }

/* ── CTA Button ────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #e50914 0%, #b0000d 100%) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(229,9,20,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(229,9,20,0.5) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Selected Movie Banner ─────────────────────────────────────────────── */
.selected-banner {
    background: linear-gradient(135deg, #0e0e1a 0%, #130a10 100%);
    border: 1px solid #252535;
    border-left: 4px solid #e50914;
    border-radius: 16px;
    padding: 22px 26px;
    display: flex;
    gap: 22px;
    align-items: flex-start;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.selected-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 50% 100% at 0% 50%, rgba(229,9,20,0.06), transparent);
}
.sel-poster-wrap img {
    width: 110px;
    border-radius: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    display: block;
}
.sel-poster-placeholder {
    width: 110px;
    height: 165px;
    border-radius: 10px;
    background: #1a1a2a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
}
.sel-info { flex: 1; position: relative; z-index: 1; }
.sel-badge {
    display: inline-block;
    background: #e50914;
    color: #fff;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.sel-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #fff;
    letter-spacing: 2px;
    line-height: 1;
    margin-bottom: 10px;
}
.sel-desc {
    color: #666;
    font-size: 0.88rem;
    line-height: 1.7;
    max-width: 600px;
}

/* ── Movie Cards ───────────────────────────────────────────────────────── */
.movie-card {
    background: #0e0e1a;
    border: 1px solid #1c1c2c;
    border-radius: 14px;
    overflow: hidden;
    position: relative;
    height: 100%;
    cursor: pointer;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.01);
    border-color: #e50914;
    box-shadow: 0 16px 40px rgba(229,9,20,0.25), 0 6px 16px rgba(0,0,0,0.5);
}
.rank-badge {
    position: absolute;
    top: 12px; left: 12px;
    background: rgba(229,9,20,0.92);
    backdrop-filter: blur(4px);
    color: #fff;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 20px;
    z-index: 3;
    letter-spacing: 0.5px;
}
.card-poster-wrap {
    position: relative;
    width: 100%;
    overflow: hidden;
}
.card-poster-wrap img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
    transition: transform 0.35s ease;
}
.movie-card:hover .card-poster-wrap img { transform: scale(1.04); }
.card-poster-placeholder {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(160deg, #12121e, #1a1a2c);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}
.card-gradient-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60%;
    background: linear-gradient(transparent, rgba(8,8,16,0.85));
    pointer-events: none;
}
.card-body {
    padding: 14px 16px 16px 16px;
}
.card-title {
    color: #e8e8f0;
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 1.3;
    margin-bottom: 10px;
    min-height: 36px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.match-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}
.match-pct {
    font-size: 0.78rem;
    font-weight: 700;
    color: #4dbd74;
}
.match-label-sm {
    font-size: 0.68rem;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.match-bar-bg {
    width: 100%;
    height: 3px;
    background: #1e1e2c;
    border-radius: 3px;
    overflow: hidden;
}
.match-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #4dbd74, #a8e063);
    border-radius: 3px;
}

/* ── How It Works Expander ─────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: #0e0e1a !important;
    border: 1px solid #1c1c2c !important;
    border-radius: 10px !important;
    color: #888 !important;
    font-size: 0.85rem !important;
}
.step-card {
    background: linear-gradient(135deg, #0e0e1a, #10101c);
    border: 1px solid #1c1c2c;
    border-left: 3px solid #e50914;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.step-num {
    font-size: 0.68rem;
    font-weight: 700;
    color: #e50914;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 5px;
}
.step-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 6px;
}
.step-desc {
    font-size: 0.84rem;
    color: #666;
    line-height: 1.65;
}
.step-desc b { color: #aaa; }

/* ── Error State ───────────────────────────────────────────────────────── */
.error-box {
    background: linear-gradient(135deg, #1a0808, #120a0a);
    border: 1px solid #4a1010;
    border-left: 4px solid #e50914;
    border-radius: 12px;
    padding: 20px 24px;
    color: #cc6666;
    font-size: 0.9rem;
    line-height: 1.7;
}
.error-box b { color: #e88; }

/* ── Footer ────────────────────────────────────────────────────────────── */
.footer-wrap {
    text-align: center;
    padding: 36px 0 16px 0;
    border-top: 1px solid #12121e;
    margin-top: 48px;
}
.footer-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #222;
    letter-spacing: 4px;
    margin-bottom: 8px;
}
.footer-logo span { color: #e50914; }
.footer-text {
    color: #333;
    font-size: 0.78rem;
    letter-spacing: 0.3px;
}
.footer-text span { color: #e50914; }
.footer-credit {
    color: #2a2a3a;
    font-size: 0.72rem;
    margin-top: 6px;
    letter-spacing: 0.3px;
}

/* ── Empty State ───────────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #2a2a38;
}
.empty-icon { font-size: 4rem; margin-bottom: 16px; opacity: 0.5; }
.empty-text { font-size: 1.1rem; font-weight: 500; color: #333; }
.empty-sub { font-size: 0.85rem; color: #2a2a38; margin-top: 6px; }

/* ── Spinner Override ──────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: #e50914 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    movies     = pd.read_csv("movies.csv")
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

data_loaded = False
try:
    movies, similarity = load_data()
    data_loaded = True
except FileNotFoundError:
    pass


# ─────────────────────────────────────────────────────────────────────────────
# TMDB POSTER HELPER
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id: int) -> str:
    if not TMDB_API_KEY or TMDB_API_KEY == "YOUR_TMDB_API_KEY":
        return PLACEHOLDER
    try:
        resp = requests.get(
            f"{TMDB_BASE}/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY},
            timeout=6,
        )
        resp.raise_for_status()
        path = resp.json().get("poster_path")
        return f"{POSTER_BASE}{path}" if path else PLACEHOLDER
    except Exception:
        return PLACEHOLDER


# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION ENGINE  (original logic, unchanged)
# ─────────────────────────────────────────────────────────────────────────────
def recommend(movie_title: str, top_n: int = 5):
    idx    = movies[movies["title"] == movie_title].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    return [
        {
            "title":    movies.iloc[i]["title"],
            "movie_id": int(movies.iloc[i]["movie_id"]),
            "score":    round(score * 100),
        }
        for i, score in scores
    ]


# ─────────────────────────────────────────────────────────────────────────────
# CARD HTML BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def build_card_html(title: str, poster_url: str, rank: int, score: int) -> str:
    bar_width = max(score, 8)
    safe_title = title.replace('"', "&quot;").replace("'", "&#39;")
    if poster_url and poster_url != PLACEHOLDER:
        media = (
            '<div class="card-poster-wrap">' +
            f'<img src="{poster_url}" alt="{safe_title}" loading="lazy">' +
            '<div class="card-gradient-overlay"></div>' +
            '</div>'
        )
    else:
        media = '<div class="card-poster-placeholder">🎬</div>'
    return (
        '<div class="movie-card">' +
        f'<div class="rank-badge">#{rank}</div>' +
        media +
        '<div class="card-body">' +
        f'<div class="card-title">{safe_title}</div>' +
        '<div class="match-row">' +
        f'<span class="match-pct">{score}% match</span>' +
        '<span class="match-label-sm">Similarity</span>' +
        '</div>' +
        '<div class="match-bar-bg">' +
        f'<div class="match-bar-fill" style="width:{bar_width}%"></div>' +
        '</div></div></div>'
    )


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████████████  LAYOUT  ████████████████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────

# ── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">🎬 &nbsp;AI-Powered · TMDB 5000 Dataset</div>
    <div class="hero-title">CINE<span>MATCH</span></div>
    <div class="hero-tagline">Intelligent movie recommendations powered by content-based filtering &amp; cosine similarity</div>
    <div class="hero-stats">
        <div class="stat-pill"><span class="stat-num">5,000+</span><span class="stat-lbl">Movies</span></div>
        <div class="stat-pill"><span class="stat-num">AI</span><span class="stat-lbl">Powered</span></div>
        <div class="stat-pill"><span class="stat-num">TMDB</span><span class="stat-lbl">Posters</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── ERROR GUARD ───────────────────────────────────────────────────────────────
if not data_loaded:
    st.markdown("""
    <div class="error-box">
        <b>⚠️  Data files not found</b><br><br>
        Could not locate <b>movies.csv</b> or <b>similarity.pkl</b>.<br>
        Run your Jupyter notebook first to generate these files, then place them
        in the same directory as <b>app.py</b> before launching Streamlit.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── CONTROLS PANEL ────────────────────────────────────────────────────────────
movie_list = sorted(movies["title"].dropna().unique().tolist())

st.markdown('<div class="control-panel">', unsafe_allow_html=True)
ctrl_left, ctrl_right, ctrl_btn = st.columns([4, 1, 1])

with ctrl_left:
    selected_movie = st.selectbox(
        "PICK A MOVIE YOU ENJOY",
        options=movie_list,
        index=movie_list.index("Avatar") if "Avatar" in movie_list else 0,
    )
with ctrl_right:
    num_recs = st.slider("RESULTS", min_value=3, max_value=10, value=5, step=1)
with ctrl_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    go = st.button("✨  Find Matches", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# ── SELECTED MOVIE BANNER ─────────────────────────────────────────────────────
with st.spinner("Loading movie info…"):
    sel_row    = movies[movies["title"] == selected_movie].iloc[0]
    sel_id     = int(sel_row["movie_id"])
    sel_poster = fetch_poster(sel_id)

if sel_poster and sel_poster != PLACEHOLDER:
    img_tag = f'<div class="sel-poster-wrap"><img src="{sel_poster}" alt="{selected_movie}"></div>'
else:
    img_tag = '<div class="sel-poster-placeholder">🎬</div>'

st.markdown(f"""
<div class="selected-banner">
    {img_tag}
    <div class="sel-info">
        <div class="sel-badge">Your Selection</div>
        <div class="sel-title">{selected_movie}</div>
        <div class="sel-desc">
            CineMatch will analyse this movie's genres, cast, director, and plot keywords
            using a 5,000-dimensional vector to find the most similar films in the database.
            Hit <b style="color:#aaa">Find Matches</b> to see your personalised list.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── RECOMMENDATIONS OUTPUT ────────────────────────────────────────────────────
if go:
    with st.spinner("🎬  Analysing content vectors and finding your best matches…"):
        recs    = recommend(selected_movie, top_n=num_recs)
        posters = [fetch_poster(r["movie_id"]) for r in recs]

    st.markdown('<p class="section-label">Recommendations</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="section-title">Because you liked <span>{selected_movie}</span></p>',
        unsafe_allow_html=True,
    )

    cols_per_row = min(num_recs, 5)

    # Build the entire grid as ONE html string — avoids st.columns() HTML rendering bug
    cards_html = f"""
    <div style="
        display: grid;
        grid-template-columns: repeat({cols_per_row}, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    ">
    """
    for i, (rec, poster) in enumerate(zip(recs, posters)):
        cards_html += build_card_html(rec["title"], poster, i + 1, rec["score"])
    cards_html += "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)

else:
    # Idle state hint
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎬</div>
        <div class="empty-text">Ready to discover your next favourite film?</div>
        <div class="empty-sub">Select a movie above and click <b>Find Matches</b></div>
    </div>
    """, unsafe_allow_html=True)


# ── HOW IT WORKS ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ️  How does the recommendation engine work?"):
    st.markdown("""
    <div class="step-card">
        <div class="step-num">Step 01 · Dataset</div>
        <div class="step-title">TMDB 5000 Movies</div>
        <div class="step-desc">
            The TMDB 5000 Movies dataset contains rich metadata for ~5,000 films — genres,
            cast, crew, keywords, and plot overviews. We merge the movies and credits tables
            on <b>title</b> to create a unified record per film.
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">Step 02 · Feature Engineering</div>
        <div class="step-title">Building Movie DNA</div>
        <div class="step-desc">
            For each movie, we construct a <b>tags</b> string by combining its overview,
            genres, plot keywords, top-3 cast names, and director — giving every film a
            rich, multi-dimensional text fingerprint that captures its essence.
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">Step 03 · Stemming</div>
        <div class="step-title">Porter Stemmer Normalisation</div>
        <div class="step-desc">
            <b>Porter Stemmer</b> reduces inflected words (e.g. "acting", "acted", "action")
            to their root form. This prevents duplicates from inflating or skewing
            similarity scores between films.
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">Step 04 · Vectorisation</div>
        <div class="step-title">CountVectorizer → Numeric Vectors</div>
        <div class="step-desc">
            <b>CountVectorizer</b> (top 5,000 words, English stop-words removed) transforms
            each movie's tag string into a numeric vector — producing a
            <b>4,806 × 5,000</b> count matrix where each cell is a word frequency.
        </div>
    </div>
    <div class="step-card">
        <div class="step-num">Step 05 · Cosine Similarity</div>
        <div class="step-title">Finding the Closest Matches</div>
        <div class="step-desc">
            We compute <b>cosine similarity</b> between every pair of movie vectors.
            Movies sharing many genres, cast members, and plot keywords have a small angle
            between their vectors (score near 1.0). We return the <b>top-N</b> closest
            matches from this pre-computed matrix — instantly, at query time.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-wrap">
    <div class="footer-logo">CINE<span>MATCH</span></div>
    <div class="footer-text">
        Built with <span>Streamlit</span> &nbsp;·&nbsp; Machine Learning
        &nbsp;·&nbsp; <span>TMDB API</span>
    </div>
    <div class="footer-credit">Nani Nulakala · AI/ML Enthusiast</div>
</div>
""", unsafe_allow_html=True)
