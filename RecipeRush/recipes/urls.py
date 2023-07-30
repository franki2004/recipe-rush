from django.conf.urls.static import static
from django.urls import path

from .views import RecipeCreateView, RecipeDetailsView, RecipeEditView, RecipeDeleteView, Index, UserRecipesDetailsView, \
    like_recipe, BrowseByCategoryView
from .. import settings

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('details/<int:pk>', RecipeDetailsView.as_view(), name='recipe-details'),
    path('edit/<int:pk>', RecipeEditView.as_view(), name='recipe-edit'),
    path('delete/<int:pk>', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('user-recipes/<int:pk>', UserRecipesDetailsView.as_view(), name='user-recipes'),
    path('like/<int:pk>', like_recipe, name='recipe-like'),
    path('browse/<str:category>', BrowseByCategoryView.as_view(), name='browse-recipes')
]
