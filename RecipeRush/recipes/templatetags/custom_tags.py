from django import template

from RecipeRush.recipes.models import Likes

register = template.Library()


@register.filter
def replace(value):
    return value.replace('-', " ").title()


@register.filter
def has_liked(recipe, user):
    return Likes.objects.filter(recipe=recipe, user=user).exists()
