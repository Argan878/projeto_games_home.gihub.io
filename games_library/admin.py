from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Game, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'cpf']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('email', 'first_name', 'last_name', 'phone_number', 'address', 'postal_code', 'region', 'city', 'street', 'street_number', 'cpf', 'profile_picture')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Importante', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'postal_code', 'region', 'city', 'street', 'street_number', 'cpf', 'profile_picture', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Game)