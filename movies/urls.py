from django.urls import path
from .views import home, get_movies,MovieDetail,recommend_view,add_comment,add_review,register,login_view,logout_view,add_to_wishlist,toggle_wishlist,wishlist_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name='home'),
    path('api/<str:category>/', get_movies, name='get_movies'),
    path('movies/<int:id>',MovieDetail,name='movie_info'),
     path('recommend/', recommend_view, name='recommend'),
      # Auth
    
      path('login/',login_view, name='login'),   # ✅ IMPORTANT
    path('register/',register, name='register'),

    # path('movie/<int:id>/',MovieDetail, name='movie_detail'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('wishlist/toggle/<int:movie_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', wishlist_view, name='wishlist'),
    # urls.py

    path('wishlist/add/<int:movie_id>/', add_to_wishlist, name='add_to_wishlist'),

path('movie/<int:movie_id>/review/', add_review, name='add_review'),
path('review/<int:review_id>/comment/', add_comment, name='add_comment'),
]
