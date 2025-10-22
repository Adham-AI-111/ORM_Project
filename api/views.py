from typing_extensions import Self
from django.db.models import query
from django.shortcuts import render
from . import serialzers
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from base.models import Restaurant, Sale, Rating
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# ---------------Restaurant Views---------------
class UserRestaurantListCreateAPIView(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serialzers.CustomRestaurantSerializer

    # filter the queryset to only include restaurants for the current user
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_permissions(self):
        self.permission_class= [AllowAny]
        if self.request.method == "POST":
            self.permission_class = [IsAuthenticated]     
    
        return super().get_permissions()    


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

# ---------------Ratings Views---------------
class RatingsListApiView(ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = serialzers.RatingsSerializer


# ---------------Sales Views---------------
class SalesListApiView(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = serialzers.SalesSerializer
    permission_classes = [IsAuthenticated]

    # filter the queryset to only include sales for the current user for his own restaurants
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(restaurant__user=self.request.user)
