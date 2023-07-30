from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as generic_views

from RecipeRush.recipes.forms import RecipeCreateForm
from RecipeRush.recipes.models import Recipe
required_login = method_decorator(login_required, name='dispatch')

# Create your views here.
class Index(generic_views.ListView):
    template_name = 'common/index.html'
    model = Recipe
    context_object_name = 'top_liked_recipes'

    def get_queryset(self):
        return Recipe.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:3]

@required_login
class RecipeCreateView(generic_views.CreateView):
    template_name = 'recipes/recipe-create.html'
    model = Recipe
    form_class = RecipeCreateForm
    success_url = reverse_lazy('user-recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDetailsView(generic_views.DetailView):
    template_name = 'recipes/recipe-details.html'
    model = Recipe
    context_object_name = 'recipe'

@required_login
class UserRecipesDetailsView(generic_views.ListView):
    model = Recipe
    template_name = 'recipes/user-recipes.html'
    context_object_name = 'user_recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

@required_login
class RecipeDeleteView(generic_views.DeleteView):
    pass

@required_login
class RecipeEditView(generic_views.UpdateView):
    pass

@required_login
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)

    if request.user.is_authenticated:
        if request.user in recipe.likes.all():
            recipe.likes.remove(request.user)
        else:
            recipe.likes.add(request.user)

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
