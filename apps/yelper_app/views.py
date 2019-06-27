from django.shortcuts import render, redirect
from ..login_registration_app.models import User
from .models import Restaurant, Review, Comment, Like, Favorite
from django.contrib import messages

# Create your views here.
def index(request):
    user = current_user(request)
    restaurants = Restaurant.objects.all()
    context = {
        'user': user,
        'restaurants': restaurants
    }
    return render(request, "yelper_app/index.html", context)

def new(request):
    user = current_user(request)
    context = {
        'user': user
    }
    return render(request, "yelper_app/new.html", context)

def create(request):
    errors = Restaurant.objects.validator(request.POST)

    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error, extra_tags=key)
        return redirect(new)
    creator = current_user(request)
    Restaurant.objects.new(request.POST, creator)
    return redirect(show)

def show(request, id):
    user = current_user(request)
    restaurant = Restaurant.objects.get(id=id)
    reviews = restaurant.reviews.all()
    context = {
        'user': user,
        'restaurant': restaurant,
        'reviews': reviews,
    }
    return render(request, "yelper_app/show.html", context)

def create_review(request, id):
    errors = Review.objects.validator(request.POST)

    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error, extra_tags=key)
        return redirect(show, id=id)
    reviewer = current_user(request)
    restaurant = Restaurant.objects.get(id=id)
    Review.objects.new(request.POST, reviewer, restaurant)
    return redirect(show, id=id)

def create_comment(request, id):
    commenter = current_user(request)
    review = Review.objects.get(id=id)
    restaurant_id = review.restaurant.id

    errors = Comment.objects.validator(request.POST)

    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error, extra_tags=key)
        return redirect(show, id=restaurant_id)

    Comment.objects.new(request.POST, commenter, review)
    return redirect(show, id=restaurant_id)

def current_user(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    return user