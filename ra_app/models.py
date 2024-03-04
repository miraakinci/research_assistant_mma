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


class FavouritePaper(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    research_question = models.CharField(max_length=255)

    def __str__(self):
        return self.title