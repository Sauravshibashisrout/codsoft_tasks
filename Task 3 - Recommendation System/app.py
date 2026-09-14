"""Content-Based Movie Recommendation System using TF-IDF and Cosine Similarity."""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #7c3aed;
    }
    .card h4 { margin: 0 0 6px 0; color: #e2e8f0; font-size: 1.05rem; }
    .card p  { margin: 2px 0; color: #94a3b8; font-size: 0.85rem; }
    .badge {
        display: inline-block;
        background: #7c3aed22;
        color: #a78bfa;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.78rem;
        margin-right: 4px;
    }
    .score { color: #34d399; font-weight: 700; }
    .star  { color: #fbbf24; }
</style>
""", unsafe_allow_html=True)


# ── Data loading & preprocessing ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(BASE_DIR / "movies.csv", sep="|").reset_index(drop=True)
    for col in ["genre", "director", "actors", "description"]:
        df[col] = df[col].fillna("")
    df["features"] = (
        df["genre"].str.replace("|", " ", regex=False) + " " +
        df["director"] + " " +
        df["actors"].str.replace("/", " ", regex=False) + " " +
        df["description"]
    )
    return df


@st.cache_data
def build_similarity(df):
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["features"])
    return cosine_similarity(matrix)


def get_recommendations(df, sim_matrix, title, genre_f, director_f, actor_f, n):
    idx = df.index[df["title"] == title].tolist()
    if not idx:
        return None, "Movie not found in dataset."

    scores = list(enumerate(sim_matrix[idx[0]]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = [(i, s) for i, s in scores if i != idx[0]]

    results = df.iloc[[i for i, _ in scores]].copy()
    results["similarity"] = [round(s * 100, 1) for _, s in scores]

    if genre_f:
        results = results[results["genre"].str.contains(genre_f, case=False, na=False)]
    if director_f:
        results = results[results["director"].str.contains(director_f, case=False, na=False)]
    if actor_f:
        results = results[results["actors"].str.contains(actor_f, case=False, na=False)]

    results = results.head(n)
    if results.empty:
        return None, "No movies match the selected filters."
    return results, None


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎬 Movie Recommender")
    st.markdown("**CodSoft AI Internship — Task 3**")
    st.divider()
    st.markdown("### How to use")
    st.markdown("""
1. Select a movie from the dropdown
2. Optionally filter by genre, director, or actor
3. Choose how many recommendations you want
4. Click **Get Recommendations**
    """)
    st.divider()
    st.markdown("### About")
    st.markdown("""
- **Algorithm:** TF-IDF + Cosine Similarity
- **Dataset:** 50 curated movies
- **Stack:** Python · Pandas · scikit-learn · Streamlit
    """)


# ── Main UI ───────────────────────────────────────────────────────────────────
st.title("🎬 Movie Recommendation System")
st.caption("Content-based recommendations powered by TF-IDF and Cosine Similarity")

df = load_data()
sim_matrix = build_similarity(df)

all_genres    = sorted({g for genres in df["genre"] for g in genres.split("|") if g})
all_directors = sorted(df["director"].unique())
all_actors    = sorted({a.strip() for actors in df["actors"] for a in actors.split("/") if a.strip()})

col1, col2 = st.columns([2, 1])

with col1:
    selected_movie = st.selectbox("🎥 Select a movie", df["title"].tolist())

with col2:
    n_recs = st.slider("Number of recommendations", 5, 10, 5)

fc1, fc2, fc3 = st.columns(3)
with fc1:
    genre_filter    = st.selectbox("🎭 Filter by genre",    [""] + all_genres)
with fc2:
    director_filter = st.selectbox("🎬 Filter by director", [""] + all_directors)
with fc3:
    actor_filter    = st.selectbox("🎭 Filter by actor",    [""] + all_actors)

st.markdown("")
if st.button("🔍 Get Recommendations", use_container_width=True, type="primary"):
    with st.spinner("Finding similar movies…"):
        recs, error = get_recommendations(
            df, sim_matrix, selected_movie,
            genre_filter, director_filter, actor_filter, n_recs
        )

    if error:
        st.warning(error)
    else:
        st.success(f"Top {len(recs)} recommendations for **{selected_movie}**")
        st.divider()
        for _, row in recs.iterrows():
            genres_html = "".join(f'<span class="badge">{g}</span>' for g in row["genre"].split("|"))
            st.markdown(f"""
<div class="card">
    <h4>{row['title']}</h4>
    <p>{genres_html}</p>
    <p>🎬 <b>Director:</b> {row['director']} &nbsp;|&nbsp; 🎭 <b>Actors:</b> {row['actors']}</p>
    <p>📖 {row['description']}</p>
    <p><span class="star">★</span> <b>{row['rating']}</b> &nbsp;|&nbsp; Match: <span class="score">{row['similarity']}%</span></p>
</div>
""", unsafe_allow_html=True)
