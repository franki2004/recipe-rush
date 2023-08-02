from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from RecipeRush.accounts.models import RecipeRushProfile
from RecipeRush.accounts.forms import RegisterUserForm, LoginUserForm, ProfileEditForm
from RecipeRush.accounts.views import AccountRegisterView, AccountLoginView, AccountLogoutView, ProfileEditView, \
    ProfileDetailsView

UserModel = get_user_model()


class AccountViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='testuser', email='testuser@example.com',
                                                 password='testpassword')

    def test_register_view(self):
        # Test AccountRegisterView
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('account-register'), data)
        self.assertEqual(response.status_code, 302)  # Check for successful registration
        self.assertTrue(UserModel.objects.filter(username='newuser').exists())  # Check if the user is created
        self.assertTrue(
            RecipeRushProfile.objects.filter(user__username='newuser').exists())  # Check if profile is created

    def test_login_view(self):
        # Test AccountLoginView
        data = {
            'username': self.user.username,
            'password': 'testpassword',
        }
        response = self.client.post(reverse('account-login'), data)
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to success_url
        self.assertTrue(response.wsgi_request.user.is_authenticated)  # Check if the user is logged in

    def test_logout_view(self):
        # Test AccountLogoutView
        self.client.login(username=self.user.username, password='testpassword')
        response = self.client.get(reverse('account-logout'))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to success_url
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Check if the user is logged out

    def test_profile_edit_view(self):
        # Test ProfileEditView
        self.client.login(username=self.user.username, password='testpassword')
        data = {
            'bio': 'This is a test bio.',
        }
        response = self.client.post(reverse('account-edit', kwargs={'pk': self.user.pk}), data)
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to success_url
        profile = RecipeRushProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'This is a test bio.')  # Check if the profile is updated

    def test_profile_details_view(self):
        # Test ProfileDetailsView
        self.client.login(username=self.user.username, password='testpassword')  # Log in the user
        response = self.client.get(reverse('account-details', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)  # Check if the view returns 200 status code
        self.assertContains(response, self.user.username)  # Check if the user's username is present in the response

    def test_account_delete_view(self):
        # Test AccountDeleteView
        self.client.login(username=self.user.username, password='testpassword')
        response = self.client.post(reverse('account-delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected to success_url
        self.assertFalse(UserModel.objects.filter(username=self.user.username).exists())  # Check if the user is deleted


class RecipeRushProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(username='testuser', email='testuser@example.com',
                                                 password='testpassword123')

    def test_profile_str_method(self):
        # Test the __str__ method of RecipeRushProfile model
        profile = RecipeRushProfile.objects.get(user=self.user)
        expected_str = f"Profile of {self.user.username}"
        self.assertEqual(str(profile), expected_str)

    def test_profile_fields(self):
        # Test the fields of RecipeRushProfile model
        profile = RecipeRushProfile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, '')
        self.assertIsNone(profile.date_of_birth)
        self.assertIsNone(profile.gender)
        # Add more assertions for other fields if present in your model
