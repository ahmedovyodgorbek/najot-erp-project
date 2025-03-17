from django.contrib.auth import get_user_model

from django.contrib import admin

UserModel = get_user_model()


@admin.register(UserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'first_name')  # Shows key fields
    list_filter = ('role', 'groups')  # Adds a filter by role in the admin panel
    search_fields = ('username', 'phone_number')  # Enables searching
