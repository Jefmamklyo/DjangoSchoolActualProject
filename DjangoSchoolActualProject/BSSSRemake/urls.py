#
#This is a app level urls.py
#


from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="view1", permanent=False)),
    path("view1/", views.View1.as_view(), name="view1"),
    path("view2/", views.View2.as_view(), name="view2"),
    path("recommendation/", views.Reccomendation.as_view(), name="recommendation"),
    path("uploads/", views.UploadFiles.as_view(), name="uploads"),

]

