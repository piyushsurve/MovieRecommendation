# 🎬 Movie Recommendation System

A full-stack Movie Recommendation System that recommends movies based on a user's selected movie. The system uses a **content-based filtering approach** to find similar movies by comparing features such as genre, cast, and movie overview.

The application also allows users to search for movies, create accounts, write reviews and comments, give ratings, and reply to other users' comments.

---

## 🚀 Features

- 🎬 Movie recommendations based on selected movies
- 🔍 Search for movies
- 🎭 Content-based movie recommendation
- ⭐ Movie ratings and reviews
- 💬 User comments
- ↩️ Reply to other users' comments
- 👤 User registration and login
- 🎥 Movie information using TMDB API
- 📱 Responsive user interface
- 🗄️ PostgreSQL database integration

---

## 🧠 Recommendation System

The project uses a **Content-Based Filtering** approach.

Movies are compared based on important features such as:

- Genre
- Cast
- Movie overview
- Other movie-related information

When a user selects a movie, the system analyzes its features and finds movies with similar characteristics.

The recommendation system uses:

- `movies.pkl` — Contains processed movie information.
- `similarity.pkl` — Contains similarity scores used to find similar movies.

The system then displays the most similar movies to the user.

---

## 🛠️ Technologies Used

### Frontend

- HTML
- Tailwind CSS
- JavaScript

### Backend

- Python
- Django
- Django REST Framework

### Database

- PostgreSQL

### API

- TMDB API

### Recommendation System

- Content-Based Filtering
- Similarity Matrix
- Machine Learning / Data Processing

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Frontend      │
                    │ HTML + Tailwind  │
                    │   + JavaScript   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Django / DRF     │
                    │     Backend      │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌─────────────┐ ┌────────────┐
       │ PostgreSQL │ │ Recommendation│ │ TMDB API  │
       │  Database  │ │    System    │ │            │
       └────────────┘ └──────┬──────┘ └────────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │  Recommended   │
                     │    Movies      │
                     └────────────────┘
