# from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    path('restaurants', views.index),
    path('restaurants/new', views.new),
    path('restaurants/create', views.create),
    path('restaurants/<int:id>', views.show),
    path('restaurants/<int:id>/create_review', views.create_review),
    path('reviews/<int:id>/create_comment', views.create_comment),
]