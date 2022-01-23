from django.contrib import admin
from .models import League, TradingHallService, TradingHallCategory, \
    Currency, UserService, UserVouch, TradingHallPrice


# Register your models here.

def make_in_active(modeladmin, request, queryset):
    queryset.update(is_active=False)


make_in_active.short_description = "Mark selected item as in active"


def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = "Mark selected item as active"


class LeagueAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    list_display = ('name', 'code', 'is_active')
    search_fields = ('name',)
    actions = [make_in_active, make_active]


class TradingHallCategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    list_display = ('title', 'is_active')
    search_fields = ('title',)
    actions = [make_in_active, make_active]


class TradingHallServiceAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'category',)
    list_display = ('title', 'category', 'is_active')
    search_fields = ('title',)
    actions = [make_in_active, make_active]


class CurrencyAdmin(admin.ModelAdmin):
    list_filter = ('league',)
    list_display = ('name', 'league', 'chaos_equivalent')
    search_fields = ('name',)


class TradingHallPriceAdmin(admin.ModelAdmin):
    list_display = ('service', 'league', 'average', 'median')
    list_filter = ('league',)


class UserServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'league', 'price', 'chaos_equivalent')
    list_filter = ('league',)
    search_fields = ('user__name',)
    actions = [make_in_active, make_active]


class UserVouchAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'receiver', 'service_name', 'karma',)
    list_filter = ('karma',)
    search_fields = ('user__name', 'service__user__name')
    readonly_fields = ('service', 'user')

    def receiver(self, obj):
        return obj.service.user

    def service_name(self, obj):
        return obj.service.service


admin.site.register(League, LeagueAdmin)
admin.site.register(TradingHallCategory, TradingHallCategoryAdmin)
admin.site.register(TradingHallService, TradingHallServiceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(TradingHallPrice, TradingHallPriceAdmin)
admin.site.register(UserService, UserServiceAdmin)
admin.site.register(UserVouch, UserVouchAdmin)
