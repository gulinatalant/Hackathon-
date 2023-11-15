from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Events(models.Model):
    title = models.CharField(max_length=130)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Events')
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=130)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True) 

    def __str__(self):
        return self.title
    

class Favourite(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE,related_name='favourite')
    favourite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favourite')



