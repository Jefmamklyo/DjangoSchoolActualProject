from django.urls import path
#import views from this file
from . import views

urlpatterns = [
    #We are visiting the root url and this defines that so no path
    path("view1/", views.view1, name="view1"),
    path("view2/", views.view1, name="view2")
]
