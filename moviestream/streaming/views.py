from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Movie, Actor, Like, Comment, WatchHistory
from django.contrib import messages

def home(request):
    hot_movies = Movie.objects.filter(is_hot=True).order_by('-created_at')[:10]
    latest_movies = Movie.objects.order_by('-release_date')[:12]
    popular_movies = Movie.objects.order_by('-views')[:12]
    
    context = {
        'hot_movies': hot_movies,
        'latest_movies': latest_movies,
        'popular_movies': popular_movies,
    }
    return render(request, 'streaming/home.html', context)

def movie_list(request):
    movies = Movie.objects.all().order_by('-created_at')
    paginator = Paginator(movies, 12)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    return render(request, 'streaming/movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments = Comment.objects.filter(movie=movie).order_by('-created_at')
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, movie=movie).exists()
        # Record view history
        WatchHistory.objects.create(user=request.user, movie=movie)
    
    movie.views += 1
    movie.save()
    
    context = {
        'movie': movie,
        'comments': comments,
        'is_liked': is_liked,
    }
    return render(request, 'streaming/movie_detail.html', context)

def actor_list(request):
    actors = Actor.objects.all().order_by('name')
    paginator = Paginator(actors, 12)
    page = request.GET.get('page')
    actors = paginator.get_page(page)
    return render(request, 'streaming/actor_list.html', {'actors': actors})

def actor_detail(request, actor_id):
    actor = get_object_or_404(Actor, id=actor_id)
    movies = actor.movies.all().order_by('-release_date')
    return render(request, 'streaming/actor_detail.html', {
        'actor': actor,
        'movies': movies
    })

def search(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(actors__name__icontains=query)
        ).distinct()
    else:
        movies = Movie.objects.none()
    
    return render(request, 'streaming/search_results.html', {
        'movies': movies,
        'query': query
    })

@login_required
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    like, created = Like.objects.get_or_create(user=request.user, movie=movie)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({'liked': liked})

@login_required
def add_comment(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        content = request.POST.get('content', '').strip()
        
        if content:
            Comment.objects.create(
                user=request.user,
                movie=movie,
                content=content
            )
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Comment cannot be empty!')
            
    return redirect('movie_detail', movie_id=movie_id)

def watch_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
    return render(request, 'streaming/watch_history.html', {'history': history})
