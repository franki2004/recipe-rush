# Generated by Django 4.2.3 on 2023-07-30 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_recipe_likes_recipe_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('main-dish', 'Main Dish'), ('side-dish', 'Side Dish'), ('starter', 'Starter'), ('salad', 'Salad'), ('soup', 'Soup'), ('dessert', 'Dessert')], max_length=9),
        ),
    ]
