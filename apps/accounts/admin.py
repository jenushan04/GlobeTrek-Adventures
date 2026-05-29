from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'date_joined')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('date_joined',)
