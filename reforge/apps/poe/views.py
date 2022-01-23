from datetime import timedelta

from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django_filters import rest_framework as filters
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import League, TradingHallCategory, TradingHallService, TradingHallPrice, UserService, \
    Currency, UserVouch
from .permissions import ReadOnly


# class BenchCraftAPIView(APIView):
#     serializer_class = serializers.BenchCraftSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self, request, league):
#         service, _ = Service.objects.get_or_create(
#             user_id=request.user.pk,
#             league=league,
#             service_type=Service.BENCH_CRAFT,
#             defaults=dict(is_available=False, price='offer'))
#         return service
#
#     def get(self, request, league=None):
#         service = self.get_object(request, league)
#         return Response(service.tags, status=status.HTTP_200_OK)
#
#     def post(self, request, league=None):
#         service = self.get_object(request, league)
#
#         serializer = serializers.BenchCraftSerializer(data=request.data)
#         serializer.is_valid()
#
#         mod = serializer.data['mod']
#
#         if serializer.data['is_remove']:
#             service.tags.remove(mod)
#         else:
#             service.tags.append(mod)
#         service.title = '%s crafts' % len(service.tags)
#         service.save()
#
#         return Response(service.tags, status=status.HTTP_200_OK)
#
#     def delete(self, request, league=None):
#         return Response([], status=status.HTTP_200_OK)


class PingAPIView(APIView):
    # serializer_class = serializers.BenchCraftSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        user = request.user

        if request.data.get('v'):
            UserService.objects.filter(user=user.profile, is_active=True).update(updated_at=now())
            return Response({'detail': 'success'}, status=status.HTTP_200_OK)

        return Response({'detail': 'fail'}, status=status.HTTP_200_OK)


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = League.objects.filter(is_active=True)
    serializer_class = serializers.LeagueSerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.filter()
    serializer_class = serializers.CurrencySerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TradingHallCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TradingHallCategory.objects.filter(is_active=True)
    serializer_class = serializers.TradingHallCategorySerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TradingHallServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TradingHallService.objects.filter()
    serializer_class = serializers.TradingHallServiceSerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TradingHallPriceViewSet(viewsets.ModelViewSet):
    queryset = TradingHallPrice.objects.all()
    serializer_class = serializers.TradingHallPriceSerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserServiceViewFilter(filters.FilterSet):
    min_item_level = filters.NumberFilter(field_name="item_level", lookup_expr='gte')

    class Meta:
        model = UserService
        fields = ['league', 'service', 'min_item_level', 'user']


class UserServiceViewSet(viewsets.ModelViewSet):
    queryset = UserService.objects.filter(is_active=True).prefetch_related('user')
    serializer_class = serializers.UserServiceSerializer
    permission_classes = [ReadOnly]
    filterset_class = UserServiceViewFilter

    def get_queryset(self):
        qs = super(UserServiceViewSet, self).get_queryset()

        if self.request.query_params.get('service'):
            half_hour_ago = now() - timedelta(minutes=30)
            qs = qs.filter(updated_at__gte=half_hour_ago)

        return qs

    @method_decorator(cache_page(20 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserServiceNoPageViewSet(UserServiceViewSet):
    pagination_class = None

    @property
    def paginator(self):
        if self.request.query_params.get('service'):
            return None

        return super().paginator


class MyServiceViewSet(viewsets.ModelViewSet):
    queryset = UserService.objects.all()
    serializer_class = serializers.UserServiceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = UserServiceViewFilter

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)

    def check_object_permissions(self, request, obj):
        return request.method in SAFE_METHODS or request.user.pk == obj.user_id


class UserVouchViewFilter(filters.FilterSet):
    receiver = filters.NumberFilter(field_name="service__user_id")

    class Meta:
        model = UserVouch
        fields = ['receiver']


class UserVouchViewSet(viewsets.ModelViewSet):
    queryset = UserVouch.objects.all()
    serializer_class = serializers.UserVouchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = UserVouchViewFilter

    # pagination_class = None

    def create(self, request, *args, **kwargs):
        data = request.data

        # TODO: rewrite as validator
        service = UserService.objects.get(pk=data['service'])

        if service.user_id == request.user.pk and not request.user.is_superuser:
            raise ValidationError('You can not vouch for yourself')

        karma = 1 if int(data.get('karma')) > 0 else -1

        if karma < 0:
            count = UserVouch.objects.filter(
                karma=karma,
                user=request.user.profile,
                updated_at__gte=now() - timedelta(minutes=30)
            ).count()

            if count > 1:
                raise ValidationError('You disapprove too much frequently, please wait 30 minutes.')

            count = UserVouch.objects.filter(
                karma=karma,
                user=request.user.profile,
                updated_at__gte=now() - timedelta(minutes=5)
            ).count()

            if count > 0:
                raise ValidationError('You disapprove too much frequently, please wait 5 minutes.')

        instance, created = UserVouch.objects.get_or_create(
            user=request.user.profile,
            service=service,
            defaults={
                'karma': data.get('karma'),
                'note': data.get('note', '')
            }
        )

        instance.karma = data['karma']
        instance.note = data.get('note', '')
        instance.save()

        serializer = self.get_serializer(instance=instance)
        # serializer.is_valid(raise_exception=False)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def check_object_permissions(self, request, obj):
        if request.method in ['DELETE', 'PATCH', 'PUT']:
            return False

        return super().check_object_permissions(request, obj)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     pass
