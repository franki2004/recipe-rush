import os

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Recipe
from .forms import RecipeCreateForm, RecipeEditForm
from .. import settings


class RecipeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com',
                                                        password='testpassword123')

    def setUp(self):
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'test-image.jpg')
        with open(image_path, 'rb') as f:
            self.image_file = SimpleUploadedFile(os.path.basename(image_path), f.read(), content_type='image/jpeg')

    def test_recipe_create_view(self):
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('recipe-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe-create.html')
        self.assertIsInstance(response.context['form'], RecipeCreateForm)

    def test_recipe_create_form(self):
        form_data = {
            'title': 'Test Recipe',
            'description': 'This is a test recipe',
            'ingredients': 'Ingredient 1, Ingredient 2, Ingredient 3',
            'instructions': 'Step 1, Step 2, Step 3',
            'category': 'main-dish',
        }
        form = RecipeCreateForm(data=form_data, files={'picture': self.image_file})
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_recipe_edit_view(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user
        )
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('recipe-edit', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe-edit.html')
        self.assertIsInstance(response.context['form'], RecipeEditForm)

    def test_recipe_edit_view_with_valid_data(self):
        # Create a recipe with an image for testing
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user,
            picture=self.image_file,
        )
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)

        # Create a dictionary containing the updated form data
        updated_image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'edited-image.png')
        with open(updated_image_path, 'rb') as f:
            updated_image_file = SimpleUploadedFile(os.path.basename(updated_image_path), f.read(),
                                                    content_type='image/png')

        # Create a dictionary containing the updated form data
        updated_form_data = {
            'title': 'Updated Recipe',
            'description': 'Updated Description',
            'ingredients': 'Ingredient 1, Ingredient 2, Ingredient 3',
            'instructions': 'Step 1, Step 2, Step 3',
            'category': 'dessert',
            'picture': updated_image_file,
        }

        response = self.client.post(reverse('recipe-edit', kwargs={'pk': recipe.pk}), data=updated_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe-details', kwargs={'pk': recipe.pk}))

        # Refresh the recipe object from the database
        recipe.refresh_from_db()

        # Assert that the recipe attributes are updated correctly, including the picture
        self.assertEqual(recipe.title, 'Updated Recipe')
        self.assertEqual(recipe.description, 'Updated Description')
        self.assertEqual(recipe.ingredients, 'Ingredient 1, Ingredient 2, Ingredient 3')
        self.assertEqual(recipe.instructions, 'Step 1, Step 2, Step 3')
        self.assertEqual(recipe.category, 'dessert')

        # Check if the picture field contains 'edited-image' in its name
        self.assertIn('edited-image', recipe.picture.name)
        self.assertEqual(updated_image_file.content_type, 'image/png')

    def test_browse_by_category_view(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user,
            picture=self.image_file,
        )
        response = self.client.get(reverse('browse-recipes', kwargs={'category': 'main-dish'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/browse-recipes.html')
        self.assertContains(response, recipe.title)

    def test_recipe_delete_view(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user
        )
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('recipe-delete', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe-delete.html')

    def test_recipe_delete_view_with_valid_data(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user
        )
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)
        response = self.client.post(reverse('recipe-delete', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-recipes', kwargs={'pk': self.user.pk}))

    def test_like_recipe_view(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test Description',
            ingredients='Ingredient 1, Ingredient 2',
            instructions='Step 1, Step 2',
            category='main-dish',
            author=self.user,
            picture=self.image_file,
        )
        login = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login)

        response = self.client.get(reverse('recipe-like', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe-details', kwargs={'pk': recipe.pk}))

        response = self.client.get(reverse('recipe-like', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipe-details', kwargs={'pk': recipe.pk}))
