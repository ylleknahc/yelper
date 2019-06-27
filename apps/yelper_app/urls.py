# from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    # url(r'^$', views.index),
    path('restaurants', views.index)
]