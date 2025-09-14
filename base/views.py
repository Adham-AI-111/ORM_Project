from django.shortcuts import render, redirect
from .models import Restaurant, Rating, Sale
from .forms import RestaurantCreationForm, RatingForm, SaleForm
from django.contrib import messages
from django.db.models import Sum

def home(request):
    '''
    The Query Set Details:
    1. Using prefetch_related to optimize the query and reduce database hits
    2. Fetching all restaurants along with their related sales and ratings in a single query
    3. This optimization is crucial for performance, especially when dealing with multiple related objects
    4. The backslash (\) is used for line continuation to enhance readability
    5. ratings queryset values contain the necessary fields to display in the template

    Filter Logic:
    1. Get filter values from GET parameters
    2. maping between display labels and stored codes for restaurant types
    3. Build a filters dictionary based on selected filters
    4. Apply combined filtering logic for rating and type filters
    5. using the resturants query to filter the ratings queryset accordingly, without filtering the ratings again
    '''
    restaurants = Restaurant.objects.prefetch_related('sales', 'ratings').all()
    # it useful for more complex queries and the filter logic below
    ratings = restaurants.values('ratings__id', 'ratings__score', 'ratings__restaurant__name', 'ratings__user__username')

    #! Get distinct restaurant types for filtering to show in the dropdown
    restaurant_types = Restaurant.objects.only('restaurant_type').distinct()
    # r is an instance of Restaurant, r.RestaurantType(r.restaurant_type).label gives the label of the enum
    # RestaurantType is the name of the enum class inside the Restaurant model
    unique_restaurant_types = set(r.RestaurantType(r.restaurant_type).label for r in restaurant_types) # return a dict of unique types
    #! ============================================
    # filter logic
    filter_rating = request.GET.get('rating_filter')
    filter_type = request.GET.get('type_filter')
    filter_sales = request.GET.get('sales_filter') 

    TYPES_MAP = [('Fast Food', 'FF'), ('Italian', 'IT'), ('Egyption', 'EG'), ('Drinks', 'DR'), ('Arabian', 'AR'), ('Other', 'OT')]

    # filters_rate_model = {}
    filters = {}
    # get the corresponding code for the selected type from the TYPES_MAP
    # this line caued error in the restaurants display #! filters['restaurant_type'] = ""
    for label, code in TYPES_MAP:
            if filter_type == label:
                filters['restaurant_type'] = code
                break
    # ! -------Combined filter logic betwee --rating-- filter and the --type-- filter-------
    # it works now 
    if filter_rating and filter_type:
        if filter_rating == "1-3" and filters['restaurant_type']:
            filters['ratings__score__lte'] = 3
            filters['restaurant_type'] = filters['restaurant_type']
        if filter_rating == "4-5" and filters['restaurant_type']:
            filters['ratings__score__in'] = (5, 4)
            filters['restaurant_type']=filters['restaurant_type']
        if filter_rating == ">=3" and filters['restaurant_type']:
            filters['ratings__score__gte'] = 3
            filters['restaurant_type']=filters['restaurant_type']
        if filter_rating == "1star" and filters['restaurant_type']:
            filters['ratings__score'] = 1
            filters['restaurant_type']=filters['restaurant_type']
    # !===================================================================================

    # ! --------Single filter logic for each filter--------------   
    # if filter_rating and not filter_type and not filter_sales:
    #     # put if condition here to check the value of filter_rating and apply the corresponding filter
    #     if filter_rating == "1-3":
    #         filters['ratings__score__lte'] = 3
    #     if filter_rating == "4-5":
    #         filters['ratings__score__in'] = (5, 4)
    #     if filter_rating == ">=3":
    #         filters['ratings__score__gte'] = 3
    #     if filter_rating == "1star":
    #         filters['ratings__score'] = 1

    # if filter_type:
    #     for label, code in TYPES_MAP:
    #         if filter_type == label:
    #             filters['restaurant_type'] = code
    #             break

    if filter_sales:
        # implement sales filter logic here based on the selected range
        if filter_sales == "<2000":
            filters['sales__amount__lt'] = 2000
        if filter_sales == "2000to4000":
            filters['sales__amount__gte'] = 2000
            filters['sales__amount__lte'] = 4000
        if filter_sales == "4000to6000":
            filters['sales__amount__gte'] = 4000
            filters['sales__amount__lte'] = 6000
        if filter_sales == ">6000":
            filters['sales__amount__gte'] = 6000
    # !-------------------------------------------------------------
    restaurants = restaurants.filter(**filters).distinct()
    ratings = restaurants.values('ratings__id', 'ratings__score', 'ratings__restaurant__name', 'ratings__user__username')
    
    context = {'restaurants': restaurants, 'ratings': ratings, 'unique_restaurant_types': unique_restaurant_types}
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
    # this -->form<-- is just to show the rating form on the same page, without go to another page
    # works by javascript its engine is in the html file and its function is in the rate_restaurant view
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
    #TODO: user = request.user
    # using "prefetch_related" to optimize the query and reduce database hits
    # the backslash (\) is used for line continuation to enhance readability
    restaurants =  \
        Restaurant.objects \
        .prefetch_related('sales')
        #TODO: .filter(user=user)
    

    # this form works like the rate_restaurant view form
    # to show the sale form on the same page, without go to another page
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