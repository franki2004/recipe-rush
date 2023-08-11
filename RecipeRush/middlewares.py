from django.urls import reverse
from RecipeRush.recipes.views import custom_404


class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            user = request.user
            if not user.is_staff:
                return custom_404(request, None)
        return self.get_response(request)
