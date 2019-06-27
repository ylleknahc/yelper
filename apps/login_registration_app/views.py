from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, 'login_registration_app/login.html')

def register(request):
    return render(request, "login_registration_app/registration.html")

def registration(request):
    errors = User.objects.validate_registration(request.POST)

    if valid_form(request, errors):
        user = User.objects.create_user(request.POST)
        # if 'user_id' not in request.session:
        request.session['user_id'] = user.id
        # else:
            # request.session['user_id'] = user.id
        return redirect('/restaurants')
    else:
        return redirect(register)

def login(request):
    errors = User.objects.validate_login(request.POST)

    if valid_form(request, errors):
        user = User.objects.fetch_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/restaurants')
    else:
        return redirect(index)

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect(index)

def valid_form(request, errors):
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error, extra_tags=f"{key}")
        return False
    else:
        return True

# def authenticated_user(request):
#     if 'user_id' not in request.session:
#         return False
#     else:
#         return True