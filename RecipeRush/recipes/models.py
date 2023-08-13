from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


class Recipe(models.Model):
    CHOICES = [
        ('main-dish', "Main Dish"),
        ('side-dish', "Side Dish"),
        ('starter', 'Starter'),
        ("salad", "Salad"),
        ('soup', 'Soup'),
        ('dessert', 'Dessert')
    ]
    title = models.CharField(null=False, blank=False, max_length=40, validators=[MinLengthValidator(3)])
    description = models.CharField(null=False, blank=False, max_length=200, validators=[MinLengthValidator(5)])
    ingredients = models.TextField(null=False, blank=False, max_length=400, validators=[MinLengthValidator(5)])
    instructions = models.TextField(null=False, blank=False, max_length=2500)
    category = models.CharField(null=False, blank=False, max_length=9, choices=CHOICES)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='recipe_pics/', null=False, blank=False)

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    commenter_name = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment_text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.commenter_name} on {self.recipe.title} - {self.timestamp}"

    def save(self, *args, **kwargs):
        if not self.id:  # Only set the commenter on object creation, not on update
            user = kwargs.pop('user', None)
            if user:
                self.commenter = user
        super().save(*args, **kwargs)
