from django.urls import path
#import views from this file
from . import views

urlpatterns = [
    #We are visiting the root url and this defines that so no path
    path("", views.index, name="index"),
]
