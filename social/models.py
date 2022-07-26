from django.db import models
from accounts.models import User


class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    subtext = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.genre_id}:{self.name}"

    class Meta:
        ordering = ('genre_id',)


class Thread(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    date_created = models.DateTimeField()
    last_update = models.DateTimeField()
    title = models.CharField(max_length=50, blank=False)
    replies = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner}:{self.title}"

    class Meta:
        ordering = ('last_update',)


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, max_length=1000)
    date_posted = models.DateTimeField()

    def __str__(self):
        return f"[{self.thread}] {self.author}:{self.content}"

    class Meta:
        ordering = ('date_posted',)
