from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Log, UserProfile, Vessel

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vessel',
        'timestamp',
        'latitude',
        'longitude',
        'destination',
        'eta'
    )
    list_display_links = list_display
    list_select_related = ('vessel',)
    list_filter = ('vessel', 'destination')

@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'ship_id',
    )
    list_display_links = list_display

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'link_to_user',
    )
    list_display_links = (
        'id',
    )
    list_select_related = ('user',)

    def link_to_user(self, obj):
        link = reverse('admin:auth_user_change', 
            args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', 
            link, obj.user.username)
    link_to_user.short_description = 'Edit user'
