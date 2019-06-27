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
    return redirect(index)

def current_user(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    return user