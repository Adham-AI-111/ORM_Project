from django.contrib.admin import action
from django.db.models import query
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from typing_extensions import Self

from base.models import Rating, Restaurant, Sale

from . import serialzers
from .filters import RatingsFilter, UserRestaurantFilter
from django_filters.rest_framework import DjangoFilterBackend


# ---------------Restaurant Views---------------
class UserRestaurantListCreateAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.CustomRestaurantSerializer
    # i use a custom filter class to let other lookups work
    filterset_class = UserRestaurantFilter
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include restaurants for the current user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    # def get_permissions(self):
    #     self.permission_class= [AllowAny]
    #     if self.request.method == "POST":
    #         self.permission_class = [IsAuthenticated]
    #     return super().get_permissions()    


class SingleRestaurantAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.CustomRestaurantSerializer
    lookup_url_kwarg = 'rest_id'
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include restaurants for the current user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
        

class AllRestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.AllRestaurantSerializer
    permission_classes = [AllowAny]
    # this backend let us search by icontains
    filter_backends = [SearchFilter, OrderingFilter]
    # only exact lookup work here in this filter
    search_fields = ['name']
    ordering_fields = ['name']


# ---------------Ratings Views---------------

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = serialzers.RatingsSerializer
    pagination_class = None
    filterset_class = RatingsFilter
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["score"]
    
    @action(
    detail=False,
    methods=['get'],
    url_path="heigher-rates",
    # permission_classes=[]
    )
    def heigher_rates(self, request):
        rates = self.get_queryset().filter(score__gte=4)
        serialzer = self.get_serializer(rates, many=True)
        return Response(serialzer.data)


# class RatingsListApiView(ListAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = serialzers.RatingsSerializer


# class RatingsOperationsApiView(RetrieveUpdateDestroyAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = serialzers.RatingsSerializer
#     lookup_url_kwarg = "rate_id"
#     permission_classes = [IsAuthenticated]


# ---------------Sales Views---------------
class SalesListApiView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = serialzers.SalesSerializer
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include sales for the current user for his own restaurants
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(restaurant__user=self.request.user)
