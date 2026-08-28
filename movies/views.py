import requests
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pickle
import os
from .models import Wishlist
from django.conf import settings
import pandas as pd
from django.contrib.auth.decorators import login_required
from .models import Review,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


movies_path = os.path.join(settings.BASE_DIR, 'movies', 'models', 'movies.pkl')
similarity_path = os.path.join(settings.BASE_DIR, 'movies', 'models', 'similarity.pkl')

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

movies = pd.DataFrame(movies)



API_KEY =  os.getenv("TMDB_API_KEY")


def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    data = requests.get(url).json()

    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return ""

def recommend(movie_name):
    movie_name = movie_name.lower()
    
    if movie_name not in movies['title'].str.lower().values:
        return []

    index = movies[movies['title'].str.lower() == movie_name].index[0]
    distances = list(enumerate(similarity[index]))

    movies_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    for i in movies_list:
        movie_data = movies.iloc[i[0]]

        recommended_movies.append({
            "id": movie_data.movie_id,   # ✅ IMPORTANT
            "title": movie_data.title,
            "poster": fetch_poster(movie_data.title)
        })

    return recommended_movies


def recommend_view(request):
    recommendations = []
    
    if request.method == "POST":
        movie = request.POST.get('movie_name')
        recommendations = recommend(movie)

    return render(request, 'recommend.html', {
        'recommendations': recommendations
    })




def fetch_movies(url):
    if "?" in url:
        url = f"{url}&api_key={API_KEY}"
    else:
        url = f"{url}?api_key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    print("URL:", url)
    print("RESULTS:", len(data.get("results", [])))  # 👈 DEBUG

    return data.get("results", [])


def home(request):
    trending = fetch_movies("https://api.themoviedb.org/3/trending/movie/week")
    horror = fetch_movies("https://api.themoviedb.org/3/discover/movie?with_genres=27")
    action = fetch_movies("https://api.themoviedb.org/3/discover/movie?with_genres=28")
    adventure = fetch_movies("https://api.themoviedb.org/3/discover/movie?with_genres=12")

    return render(request, "home.html", {
        "trending_movies": trending,
        "horror_movies": horror,
        "action_movies": action,
        "adventure_movies": adventure,
    })


@api_view(['GET'])
def get_movies(request, category):
    urls = {
        "trending": "https://api.themoviedb.org/3/trending/movie/week",
        "horror": "https://api.themoviedb.org/3/discover/movie?with_genres=27",
        "action": "https://api.themoviedb.org/3/discover/movie?with_genres=28",
        "adventure": "https://api.themoviedb.org/3/discover/movie?with_genres=12",
    }

    url = urls.get(category)
    if not url:
        return Response([])

    response = requests.get(f"{url}&api_key={API_KEY}")
    data = response.json()

    return Response(data.get("results", []))


def MovieDetail(request, id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}"
    video_url = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={API_KEY}"
    response = requests.get(url)
    video_data = requests.get(video_url).json()
    reviews = Review.objects.filter(movie_id=id)


    trailer_key = None
    trailer_url = None

    for video in video_data.get("results", []):
       if video["type"] == "Trailer" and video["site"] == "YouTube":
          trailer_key = video["key"]
          trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
          break

    # Make sure we parse JSON
    try:
        data = response.json()
    except ValueError:
        data = {}  # fallback to empty dict

    # Ensure data is a dictionary before adding new keys
    if isinstance(data, dict):
        # Optional: add media_type key
        data["media_type"] = "Movie"

        # Convert runtime to hours and minutes
        if data.get("runtime"):
            runtime = data["runtime"]
            hours = runtime // 60
            minutes = runtime % 60
            data["runtime_hours"] = hours
            data["runtime_minutes"] = minutes
        else:
            data["runtime_hours"] = None
            data["runtime_minutes"] = None
    else:
        data = {}  # fallback if response is not a dict

    return render(request, 'movie_detail.html', {'Data': data, "trailer_key": trailer_key,'reviews': reviews})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors) 

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def add_to_wishlist(request, movie_id):
    title = request.POST.get('title')
    poster = request.POST.get('poster')

    Wishlist.objects.get_or_create(
        user=request.user,
        movie_id=movie_id,
        defaults={
            'title': title,
            'poster_path': poster
        }
    )

    return redirect('movie_info', id=movie_id)

@login_required(login_url='login')
def add_review(request, movie_id):
    if request.method == "POST":
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        print(request.POST)

        Review.objects.create(
            user=request.user,
            movie_id=movie_id,
            content=content,
            rating=rating
        )

    return redirect('movie_info', id=movie_id)

@login_required(login_url='login')
def add_comment(request, review_id):
    if request.method == "POST":
        content = request.POST.get('content')
        review = Review.objects.get(id=review_id)
        print(request.POST)

        Comment.objects.create(
            user=request.user,
            review=review,
            content=content
        )

    return redirect('movie_info', id=review.movie_id)


@login_required(login_url='login')
def toggle_wishlist(request, movie_id):
    title = request.POST.get('title')
    poster = request.POST.get('poster')

    obj, created = Wishlist.objects.get_or_create(
        user=request.user,
        movie_id=movie_id,
        defaults={
            'title': title,
            'poster_path': poster
        }
    )

    # If already exists → remove
    if not created:
        obj.delete()

    return redirect('movie_info', id=movie_id)


# ✅ SHOW WISHLIST PAGE
@login_required(login_url='login')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required(login_url='login')
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})
