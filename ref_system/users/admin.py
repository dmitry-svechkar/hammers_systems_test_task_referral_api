from django.contrib import admin
from users.models import CustomUserModel


@admin.register(CustomUserModel)
class UserAdmin(admin.ModelAdmin):
    pass
