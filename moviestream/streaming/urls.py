from django.urls import path
from . import views

app_name = 'streaming'

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('actors/', views.actor_list, name='actor_list'),
    path('actor/<int:actor_id>/', views.actor_detail, name='actor_detail'),
    path('search/', views.search, name='search'),
    path('movie/<int:movie_id>/like/', views.toggle_like, name='toggle_like'),
    path('movie/<int:movie_id>/comment/', views.add_comment, name='add_comment'),
    path('history/', views.watch_history, name='watch_history'),
]
