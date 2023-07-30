from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

UserModel = get_user_model()


# Create your models here.
class Recipe(models.Model):
    CHOICES = [
        ('main-dish', "Main Dish"),
        ('side-dish', "Side Dish"),
        ('starter', 'Starter'),
        ("salad", "Salad"),
        ('soup', 'Soup'),
        ('dessert', 'Dessert')
    ]
    title = models.CharField(null=False, blank=False, max_length=30, validators=[MinLengthValidator(3)])
    description = models.CharField(null=False, blank=False, max_length=200, validators=[MinLengthValidator(5)])
    ingredients = models.TextField(null=False, blank=False, max_length=400, validators=[MinLengthValidator(5)])
    instructions = models.TextField(null=False, blank=False, max_length=2500)
    category = models.CharField(null=False, blank=False, max_length=9, choices=CHOICES)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(UserModel, related_name='like_recipes', blank=True)
    picture = models.ImageField(upload_to='recipe_pics/', null=False, blank=False)

    def __str__(self):
        return self.title
