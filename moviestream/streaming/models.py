from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Actor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    poster = models.URLField()
    video_url = models.URLField()
    actors = models.ManyToManyField(Actor, related_name='movies')
    is_hot = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'movie')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.movie.title}'

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(default=timezone.now)
    watch_duration = models.IntegerField(default=0)  # Duration watched in seconds

    class Meta:
        verbose_name_plural = 'Watch histories'
        ordering = ['-watched_at']

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'
