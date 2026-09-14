# Task 3 — Content-Based Movie Recommendation System

A Streamlit app that recommends movies using **TF-IDF vectorization** and **cosine similarity** on combined movie metadata (genre, director, actors, description).

## Features

- Search and select any movie from the dataset
- Filter recommendations by genre, director, or actor
- Slider to control number of recommendations (5–10)
- Clean card-based UI with similarity score and star rating
- Graceful handling of missing data and no-result cases

## Stack

| Layer | Tech |
|-------|------|
| UI | Streamlit |
| Data | Pandas |
| ML | scikit-learn (TF-IDF + Cosine Similarity) |
| Dataset | 50 curated movies (`movies.csv`) |

## Setup & Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
Task 3 - Recommendation System/
├── app.py           # Main Streamlit application
├── movies.csv       # Sample dataset (50 movies)
├── requirements.txt
└── README.md
```
