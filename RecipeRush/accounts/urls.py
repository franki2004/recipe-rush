from django.urls import path

from RecipeRush.accounts.views import ProfileDetailsView, AccountRegisterView, AccountLoginView, AccountLogoutView, \
    ProfileEditView, AccountDeleteView

urlpatterns = [
    path('<int:pk>', ProfileDetailsView.as_view(), name='account-details'),
    path('register/', AccountRegisterView.as_view(), name='account-register'),
    path('login/', AccountLoginView.as_view(), name='account-login'),
    path('logout/', AccountLogoutView.as_view(), name='account-logout'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='account-edit'),
    path('delete/<int:pk>', AccountDeleteView.as_view(), name='account-delete')
]
