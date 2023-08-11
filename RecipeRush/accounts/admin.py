from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import RecipeRushProfile

# Register your models here.
UserModel = get_user_model()


class RecipeRushUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-pk',)
    filter_horizontal = ('groups', 'user_permissions',)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        user = form.instance

        if user.groups.filter(name__in=['Moderators', 'Admins']).exists():
            user.is_staff = True
            user.save()
        else:
            user.is_staff = False
            user.save()

class RecipeRushProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender')
    list_filter = ('gender',)
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)


admin.site.register(UserModel, RecipeRushUserAdmin)
admin.site.register(RecipeRushProfile, RecipeRushProfileAdmin)
