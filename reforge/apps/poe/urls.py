from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
# router.register(r'vouches', views.VouchViewSet)
router.register(r'leagues', views.LeagueViewSet)
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'categories', views.TradingHallCategoryViewSet)
router.register(r'hall-services', views.TradingHallServiceViewSet)
router.register(r'hall-services', views.TradingHallServiceViewSet)
router.register(r'hall-prices', views.TradingHallPriceViewSet)
router.register(r'my-services', views.MyServiceViewSet)
router.register(r'user-services', views.UserServiceViewSet)
router.register(r'user-services-2', views.UserServiceNoPageViewSet)
router.register(r'vouches', views.UserVouchViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^ping/?$', views.PingAPIView.as_view()),
    # url(r'^bench/(?P<league>.+)/?$', views.BenchCraftAPIView.as_view())
]
