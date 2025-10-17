from django.db.models import query
from django.shortcuts import render
from . import serialzers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from base.models import Restaurant, Sale, Rating
from rest_framework.permissions import IsAuthenticated


class RestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.RestaurantSerializer
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include restaurants for the current user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class SingleRestaurantAPIView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.RestaurantSerializer
    lookup_url_kwarg = 'rest_id'

class RatingsListApiView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = serialzers.RatingsSerializer

class SalesListApiView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = serialzers.SalesSerializer
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include sales for the current user for his own restaurants
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(restaurant__user=self.request.user)
