from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login, get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as generic_views
from RecipeRush.accounts.forms import RegisterUserForm, LoginUserForm, ProfileEditForm
from RecipeRush.accounts.models import RecipeRushProfile

required_login = method_decorator(login_required, name='dispatch')
UserModel = get_user_model()


@required_login
class ProfileDetailsView(generic_views.DetailView):
    template_name = 'accounts/user-details.html'
    model = RecipeRushProfile

    def get_queryset(self):
        return RecipeRushProfile.objects.filter(user_id=self.kwargs['pk'])


class AccountRegisterView(generic_views.CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class AccountLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('index')


@required_login
class AccountLogoutView(auth_views.LogoutView):
    pass


@required_login
class ProfileEditView(generic_views.UpdateView):
    template_name = 'accounts/user-edit.html'
    form_class = ProfileEditForm
    model = RecipeRushProfile

    def get_object(self, queryset=None):
        return get_object_or_404(RecipeRushProfile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('account-details', kwargs={'pk': self.request.user.pk})


@required_login
class AccountDeleteView(generic_views.DeleteView):
    template_name = 'accounts/user-delete.html'
    model = UserModel
    success_url = reverse_lazy('index')
