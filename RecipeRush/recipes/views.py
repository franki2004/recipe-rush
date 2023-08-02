from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as generic_views

from RecipeRush.recipes.forms import RecipeCreateForm, RecipeEditForm, CommentForm
from RecipeRush.recipes.models import Recipe, Likes, Comment

required_login = method_decorator(login_required, name='dispatch')
UserModel = get_user_model()


# Create your views here.
class Index(generic_views.ListView):
    template_name = 'common/index.html'
    context_object_name = 'top_liked_recipes'

    def get_queryset(self):
        # Get the top 3 most liked recipes
        return Recipe.objects.annotate(num_likes=Count('likes__recipe')).order_by('-num_likes')[:3]


@required_login
class RecipeCreateView(generic_views.CreateView):
    template_name = 'recipes/recipe-create.html'
    model = Recipe
    form_class = RecipeCreateForm

    def get_success_url(self):
        return reverse_lazy('user-recipes', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDetailsView(generic_views.DetailView):
    template_name = 'recipes/recipe-details.html'
    model = Recipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data['comment_text']
            commenter_name = request.user  # Assuming the user is logged in
            comment = Comment.objects.create(recipe=recipe, commenter_name=commenter_name, comment_text=comment_text)
            # You can also set the timestamp field here if needed

        # Refresh the recipe object from the database to include the new comment
        recipe.refresh_from_db()

        context = {
            'recipe': recipe,
            'comment_form': comment_form,
        }

        return render(request, 'recipes/recipe-details.html', context)


@required_login
class UserRecipesDetailsView(generic_views.ListView):
    model = Recipe
    template_name = 'recipes/user-recipes.html'
    context_object_name = 'user_recipes'

    def get_queryset(self):
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(UserModel, pk=user_pk)
        return Recipe.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        user = get_object_or_404(UserModel, pk=user_pk)
        context['author_name'] = user.username
        return context


@required_login
class RecipeDeleteView(generic_views.DeleteView):
    model = Recipe
    template_name = 'recipes/recipe-delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('user-recipes', kwargs={'pk': self.request.user.pk})


@required_login
class RecipeEditView(generic_views.UpdateView):
    model = Recipe
    template_name = 'recipes/recipe-edit.html'
    form_class = RecipeEditForm

    def get_success_url(self):
        return reverse_lazy('recipe-details', kwargs={'pk': self.kwargs['pk']})


@login_required
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if Likes.objects.filter(user=request.user, recipe=recipe).exists():
        Likes.objects.filter(user=request.user, recipe=recipe).delete()
    else:
        Likes.objects.create(user=request.user, recipe=recipe)

    # Redirect back to the recipe detail page after liking/unliking
    return redirect('recipe-details', pk=pk)


class BrowseByCategoryView(generic_views.ListView):
    model = Recipe
    template_name = 'recipes/browse-recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        category = self.kwargs['category']
        return Recipe.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        context['category'] = category  # Add the category to the context
        return context


@required_login
class LikedRecipesView(generic_views.ListView):
    template_name = 'recipes/recipe-liked.html'
    context_object_name = 'liked_recipes'

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(likes__user=user)


def custom_404(request, exception):
    return render(request, 'common/404.html', status=404)


class CommentDeleteView(generic_views.View):
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('recipe-details', pk=comment.recipe.pk)
