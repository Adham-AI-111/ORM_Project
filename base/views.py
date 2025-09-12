from django.shortcuts import render, redirect
from .models import Restaurant, Rating, Sale
from .forms import RestaurantCreationForm, RatingForm, SaleForm
from django.contrib import messages
from django.db.models import Sum

def home(request):
    restaurants = Restaurant.objects.all()
    ratings = Rating.objects.all()
    context = {'restaurants': restaurants, 'ratings': ratings}
    return render(request, 'base/home.html', context)

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = request.user  # Assuming the user is logged in
            restaurant.save()
            messages.success(request, 'Restaurant added successfully!')
            return redirect('home')
    else:
        form = RestaurantCreationForm()
    context = {'form': form}
    return render(request, 'base/add_restaurant.html', context)

def edit_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant updated successfully!')
            return redirect('home')
    else:
        form = RestaurantCreationForm(instance=restaurant)
    context = {'form': form, 'restaurant': restaurant}
    return render(request, 'base/edit_restaurant.html', context)

def delete_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, 'Restaurant deleted successfully!')
        return redirect('home')
    context = {'restaurant': restaurant}
    return render(request, 'base/delete.html', context)

def display_restaurants_to_rate(request):
    rests = Restaurant.objects.all()
    form = RatingForm()
    context = {'rests': rests, 'form': form}
    return render(request, 'base/display_rest_to_rate.html', context)

def rate_restaurant(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # Avoid duplicate ratings per user per restaurant: update if exists, else create
            rating_value = form.cleaned_data['score']
            rating_obj, created = Rating.objects.update_or_create(
                user=request.user,
                restaurant=restaurant,
                defaults={'score': rating_value},
            )
            messages.success(request, 'Thank you for your rating!')
            return redirect('rate_restuarant')
    else:
        form = RatingForm()
    context = {'form': form, 'restaurant': restaurant}
    return render(request, 'base/add_rate.html', context)

def restaurant_sale(request):
    user = request.user
    restaurants = (
        Restaurant.objects
        .filter(user=user)
        .prefetch_related('sales')
    )
    form = SaleForm()

    context = {"restaurants": restaurants, "form": form}
    return render(request, 'base/rest_sales.html', context)

def add_sales(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            amount_value = form.cleaned_data['amount']
            date_value = form.cleaned_data['date']
            # Avoid duplicate sales entries: create only if not exists
            new_sale, created = Sale.objects.get_or_create(
                restaurant=restaurant,
                amount=amount_value,
                date=date_value,
            )
            messages.success(request, 'Sale record added successfully!')
            return redirect('view_restaurant_sale')
    else:
        form = SaleForm()
    context = {'form': form, 'restaurant': restaurant}
    return render(request, 'base/add_sales.html', context)