from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma', 'positive_karma', 'unique_positive', 'negative_karma', 'unique_negative')


admin.site.register(Profile, ProfileAdmin)
