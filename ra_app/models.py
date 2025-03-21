from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, null=False, blank=False,
        validators=[RegexValidator(
            regex=r'^.{5,}$',
            message='Username must contain at least 5 characters'
        )]
    )
    email = models.EmailField(unique=True, null=False, blank=False,
        validators=[EmailValidator(
            message="Please enter a valid email address"
        )]
    )
    bio = models.TextField(max_length=200, blank=True)


class Article(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, default='Unknown Author')
    link = models.URLField(max_length=200)
    publication_info = models.CharField(max_length=255, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    favourited_by = models.ManyToManyField(User, related_name="favourite_articles", blank=True)

    def __str__(self):
        return self.title


class FavouritePaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favourites", null=True, blank=True)

    def __str__(self):
        if self.article:
            return self.article.title
        return "Unknown Article"