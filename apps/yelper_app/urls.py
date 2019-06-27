# from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('restaurants', views.index),
    path('restaurants/new', views.new),
    path('restaurants/create', views.create),
]