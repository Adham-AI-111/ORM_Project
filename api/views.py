from django.shortcuts import render
from . import serialzers
from rest_framework.generics import ListAPIView
from base.models import Restaurant, Sale, Rating


class RestaurantListAPIView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.RestaurantSerializer

class RatingsListApiView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = serialzers.RatingsSerializer

class SalesListApiView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = serialzers.SalesSerializer
