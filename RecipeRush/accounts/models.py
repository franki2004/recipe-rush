from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model


class RecipeRushUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(username, email, password, **extra_fields)


class RecipeRushUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username = models.CharField(max_length=20, validators=[MinLengthValidator(4)], unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RecipeRushUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

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
    first_name = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    last_name = models.CharField(max_length=20, validators=[MinLengthValidator(2)], null=True, blank=True)
    user_picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
