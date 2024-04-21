from django.contrib import admin

from users.models import CustomUserModel


@admin.register(CustomUserModel)
class UserAdmin(admin.ModelAdmin):
    """ Настройка отображения админ панели. """
    list_display = (
        'reg_data',
        'telephone_number',
        'is_active',
        'user_referal_code',
        'invitation_code'
    )
    search_fields = ('telephone_number',)
    ordering = ('-reg_data',)
    fields = [
        'telephone_number', 'is_active',
        ('user_referal_code', 'invitation_code')
    ]
