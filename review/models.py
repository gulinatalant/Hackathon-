from django.db import models
from django.contrib.auth import get_user_model
from events.models import Events

User = get_user_model()


class Comment(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    event = models.ForeignKey(Events, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body} - {self.event}'


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField()
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='ratings')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return f'{self.rating}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.author.username} liked {self.event.title}'
