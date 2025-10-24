from django.shortcuts import render, redirect
from .models import Restaurant, Rating, Sale
from .forms import RestaurantCreationForm, RatingForm, SaleForm
from django.contrib import messages
# from django.db.models import Sum,  Avg
from django.db.models import Case, When, Value, CharField, Q, Avg



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
    # it useful for more complex queries and the filter logic below, beacause we will filter the restaurants queryset
    ratings = restaurants.values('ratings__id', 'ratings__score', 'ratings__restaurant__name', 'ratings__user__username')

    #! Get distinct restaurant types for filtering to show in the dropdown
    restaurant_types = Restaurant.objects.only('restaurant_type').distinct()
    # r is an instance of Restaurant, r.RestaurantType(r.restaurant_type).label gives the label of the enum
    # RestaurantType is the name of the enum class inside the Restaurant model
    unique_restaurant_types = set(r.RestaurantType(r.restaurant_type).label for r in restaurant_types) # return a dict of unique types
    #! ============================================
    # filter logic
    filter_rating = request.GET.get('rating_filter')
    filter_type = request.GET.getlist('type_filter')
    print(filter_type)
    filter_sales = request.GET.get('sales_filter') 

    filters = {}
    '''
    Filter Logic Explanation:
    1. Get filter parameters from URL query string (rating, type, sales)
    2. Map user-friendly restaurant types (e.g., 'Fast Food') to database codes ('FF')
    3. Convert selected types to their corresponding database codes using list comprehension
    4. Build a dynamic filters dictionary for the Restaurant.objects.filter() query
    5. Apply filters only if they are selected by the user, otherwise return all restaurants

    Combined Filter Logic (Rating + Type):
    - Handles three scenarios:
        1. Both rating AND type filters selected:
            - Preserves restaurant_type filter
            - Adds rating filter based on selection:
             * "1-3": ratings <= 3
             * "4-5": ratings in [4,5]
             * ">=3": ratings >= 3
             * "1star": ratings = 1
        
        2. Only rating filter selected (no type):
            - Applies rating criteria without type restriction
        
        3. Only type filter selected:
            - Filters by restaurant type only

    This approach allows for:
    - Flexible combination of filters
    - Precise control over rating ranges
    - Maintaining filter context when both are active
    - Independent operation when only one filter is selected
    '''
    TYPES_MAP = [('Fast Food', 'FF'), ('Italian', 'IT'), ('Egyption', 'EG'), ('Drinks', 'DR'), ('Arabian', 'AR'), ('Other', 'OT')]
    label_to_code = dict(TYPES_MAP)
    # this will apply the type filter every time, combined with the score filter by the if condition, and single also
    if filter_type:
        # using list comperhension and __in instead of looping towice
        chosen_value_type = [label_to_code[t] for t in filter_type if t in label_to_code]
        filters['restaurant_type__in'] = chosen_value_type

    # ---------------------------------------------
    #? !OLD WAY TO: filtering the restaurants based on types that are choosen
    # chosen_value_type = []
    # if filter_type: # 2. check if there are values in filter_type 
    #     for label, code in TYPES_MAP: # 1. get the types in DB 
    #     # TODO: get list of filter values for rst type
    #         for type in filter_type:  # get the types that were found
    #             if type == label:
    #                 chosen_value_type.append(code)
    #     filters['restaurant_type__in'] = chosen_value_type # we will get several version from this filter if there are more that on value

    # ! new filter-------Combined filter logic betwee --rating-- filter and the --type-- filter-------
    # it works now 
    #  -----------------------------------------

    # check if the score and type filter are chosen together; it is not necessary to check the type every time you check the score
    if filter_rating and filter_type:
        # Restaurant type filter is already set above, just add rating filter
        if filter_rating == "1-3":
            filters['ratings__score__lte'] = 3
        if filter_rating == "4-5":
            filters['ratings__score__in'] = (5, 4)
        if filter_rating == ">=3":
            filters['ratings__score__gte'] = 3
        if filter_rating == "1star":
            filters['ratings__score'] = 1
    elif filter_rating and not filter_type:
        if filter_rating == "1-3" :
            filters['ratings__score__lte'] = 3
        if filter_rating == "4-5":
            filters['ratings__score__in'] = (5, 4)
        if filter_rating == ">=3":
            filters['ratings__score__gte'] = 3
        if filter_rating == "1star":
            filters['ratings__score'] = 1
    # !-------------------------------------------------------------

    # ! old filter --------Single filter logic for each filter--------------   
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
            filters['sales__income__lt'] = 2000
        if filter_sales == "2000to4000":
            filters['sales__income__gte'] = 2000
            filters['sales__income__lte'] = 4000
        if filter_sales == "4000to6000":
            filters['sales__income__gte'] = 4000
            filters['sales__income__lte'] = 6000
        if filter_sales == ">6000":
            filters['sales__income__gte'] = 6000
    # !-------------------------------------------------------------
    # ! --------------------search logic----------------------------
    q = request.GET.get('q')
    q_value = Q()
    if q:
        q_value = Q(name__icontains=q) | Q(restaurant_type__icontains=q) | Q(user__username__icontains=q)
    restaurants = restaurants.filter(q_value, **filters).distinct()
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
    # i replaced this query to increase the performance while i did not want all the db atb
    # rests = Restaurant.objects.all()
    
    # using Case,When,then to catch the full type name, because values() cannot get the full name while we use a choice class
    rests = Restaurant.objects.annotate(
    rest_type_display=Case(
        When(restaurant_type='FF', then=Value('Fast Food')),
        When(restaurant_type='IT', then=Value('Italian')),
        When(restaurant_type='EG', then=Value('Egyption')),
        When(restaurant_type='DR', then=Value('Drinks')),
        When(restaurant_type='AR', then=Value('Arabian')),
        When(restaurant_type='OT', then=Value('Other')),
        output_field=CharField()
    )).values('id', 'name', 'rest_type_display', 'restaurant_type')
    # add avg_rates to the rests queryset
    rests = rests.annotate(avg_rates=Avg('ratings__score'))

    # this -->form<-- is just to show the rating form on the same page, without go to another page
    # works by javascript its engine is in the html file and its function is in the rate_restaurant view
    form = RatingForm()

    q = request.GET.get('q')
    q_values = Q()
    if q:
        q_values = Q(name__icontains=q) | Q(date__icontains=q)

    rests = rests.filter(q_values)
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
    # using "prefetch_related" to optimize the query and reduce database hits
    # the backslash (\) is used for line continuation to enhance readability
    restaurants =  \
        Restaurant.objects \
        .prefetch_related('sales')
        #TODO: .filter(user=user)
    

    # this form works like the rate_restaurant view form
    # to show the sale form on the same page, without go to another page
    form = SaleForm()
    q = request.GET.get('q')
    q_values = Q()
    if q:
        q_values = Q(name__icontains=q) 
        
    restaurants = restaurants.filter(q_values)
    context = {"restaurants": restaurants, "form": form}
    return render(request, 'base/rest_sales.html', context)

def add_sales(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            income_value = form.cleaned_data['income']
            date_value = form.cleaned_data['date']
            # Avoid duplicate sales entries: create only if not exists
            new_sale, created = Sale.objects.get_or_create(
                restaurant=restaurant,
                income=income_value,
                date=date_value,
            )
            messages.success(request, 'Sale record added successfully!')
            return redirect('view_restaurant_sale')
    else:
        form = SaleForm()
    context = {'form': form, 'restaurant': restaurant}
    return render(request, 'base/add_sales.html', context)