from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from RecipeRush import settings
from RecipeRush.recipes.views import Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RecipeRush.recipes.urls')),
    path('account/', include('RecipeRush.accounts.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
