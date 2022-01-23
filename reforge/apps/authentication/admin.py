from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    exclude = ('password', 'last_login')
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
