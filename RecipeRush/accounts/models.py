from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model


class RecipeRushUser(auth_models.AbstractUser):
    username = models.CharField(max_length=20, validators=[MinLengthValidator(4)], null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    last_name = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    user_picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.username


UserModel = get_user_model()


class RecipeRushProfile(models.Model):
    CHOICES = [
        ('M', "Male"),
        ('F', "Female"),
        ("O", "Other")
    ]

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(null=True, blank=True, max_length=1, choices=CHOICES)

    def __str__(self):
        return f"Profile of {self.user.username}"
