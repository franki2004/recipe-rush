from django.conf.urls.static import static
from django.urls import path

from .views import RecipeCreateView, RecipeDetailsView, RecipeEditView, RecipeDeleteView, Index, UserRecipesDetailsView, \
    like_recipe, BrowseByCategoryView, LikedRecipesView, CommentDeleteView
from .. import settings

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create-recipe/', RecipeCreateView.as_view(), name='recipe-create'),
    path('details-recipe/<int:pk>', RecipeDetailsView.as_view(), name='recipe-details'),
    path('edit-recipe/<int:pk>', RecipeEditView.as_view(), name='recipe-edit'),
    path('delete-recipe/<int:pk>', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('user-recipes/<int:pk>', UserRecipesDetailsView.as_view(), name='user-recipes'),
    path('recipe/like/<int:pk>/', like_recipe, name='recipe-like'),
    path('browse-recipes/<str:category>', BrowseByCategoryView.as_view(), name='browse-recipes'),
    path('liked-recipes/', LikedRecipesView.as_view(), name='liked-recipes'),
    path('comment-delete/<int:pk>', CommentDeleteView.as_view(), name='comment-delete')
]
