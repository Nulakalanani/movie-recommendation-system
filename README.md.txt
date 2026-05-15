# 🎬 CineMatch – AI Movie Recommendation System

CineMatch is an AI-powered movie recommendation web application that suggests similar movies using **content-based filtering**, **natural language processing (NLP)**, and **cosine similarity**.

The application analyzes movie metadata such as genres, keywords, cast, crew, and plot overviews to generate intelligent recommendations through an interactive Streamlit interface.

🔗 **Live Demo:** *(Add your deployed Streamlit link here after deployment)*

---

## 🚀 Features

* 🎥 AI-powered movie recommendations
* 🧠 Content-Based Filtering
* 📊 Cosine Similarity recommendation engine
* 📝 NLP preprocessing using CountVectorizer & Porter Stemmer
* 🖼️ Dynamic movie posters using TMDB API
* 🌙 Modern dark-themed Streamlit UI
* ⚡ Fast recommendation retrieval using precomputed similarity matrix
* 📱 Responsive and interactive interface

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Libraries & Frameworks

* Streamlit
* Pandas
* NumPy
* Scikit-learn
* NLTK
* Requests

### Machine Learning Concepts Used

* NLP Preprocessing
* CountVectorizer
* Cosine Similarity
* Feature Engineering
* Content-Based Recommendation Systems

### API

* TMDB API

---

## 🧠 How the Recommendation System Works

1. Merge movie and credits datasets
2. Extract important features:

   * Genres
   * Keywords
   * Cast
   * Director
   * Overview
3. Combine features into a single `tags` column
4. Apply text preprocessing and stemming
5. Convert text into vectors using CountVectorizer
6. Compute cosine similarity between movie vectors
7. Recommend movies with highest similarity scores

---

## 📂 Project Structure

```bash
Recommendation-System/
│
├── app.py
├── movies.csv
├── similarity.pkl
├── requirements.txt
├── README.md
├── .gitignore
│
├── notebooks/
│   └── movie_recommendation.ipynb
│
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── assets/
    └── screenshot.png
```

---

## ▶️ Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
```

### 2. Navigate to Project Folder

```bash
cd movie-recommendation-system
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit App

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project is deployed using **Streamlit Community Cloud**.

After deployment, the live application link can be accessed from the **Live Demo** section at the top of this README.

---

## 📊 Dataset

Dataset used:

* TMDB 5000 Movies Dataset

Source:
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

---

## 🤖 AI-Assisted Development

The Streamlit frontend UI styling, layout enhancements, and parts of the development workflow were created with AI-assisted development tools for learning, rapid prototyping, and UI enhancement purposes.

The machine learning pipeline, preprocessing workflow, recommendation logic understanding, and project customization were implemented and learned during the development process.

---

## 📸 Preview

(Add your deployed app screenshots here)

---

## 👨‍💻 Author

Nani
BTech – Data Science
Raghu Engineering College

---

## ⭐ Future Improvements

* Collaborative Filtering
* User Authentication
* Personalized Recommendations
* Search Autocomplete
* Hybrid Recommendation System
* Deep Learning-based Recommendations

---
