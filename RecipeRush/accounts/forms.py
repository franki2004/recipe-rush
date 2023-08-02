from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from RecipeRush.accounts.models import RecipeRushProfile

UserModel = get_user_model()


class LoginUserForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-user", 'placeholder': "Username"}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", 'placeholder': "Password"}),
        required=True)


class RegisterUserForm(auth_forms.UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Username'}),
        required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': "Email Address"}),
        required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Password"}),
        required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Repeat Password"}),
        required=True)

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                               'placeholder': 'First Name'}),
                                 required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user',
                                                              'placeholder': 'Last Name'}),
                                required=False)

    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-user',
                                     'placeholder': 'Bio', 'style': 'height: 80px'}),
        required=False)

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'form-control form-control-user', 'placeholder': 'Date of Birth', 'type': 'date'}),
        required=False)

    gender = forms.TypedChoiceField(choices=RecipeRushProfile.CHOICES,
                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                    coerce=str,
                                    required=False)

    user_picture = forms.URLField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Profile Picture URL'}),
        required=False,
        label='Profile Picture URL'
    )

    class Meta:
        model = RecipeRushProfile
        fields = ('first_name', 'last_name', 'bio', 'date_of_birth', 'gender', 'user_picture')

