#
#This is a app level urls.py
#


from django.urls import path
from .views import View1, View2, Reccomendation, UploadFiles, loginView, logOutView
from django.views.generic import RedirectView    


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="view1", permanent=False)),
    path("view1/", View1.as_view(), name="view1"),
    path("view2/", View2.as_view(), name="view2"),
    path("recommendation/", Reccomendation.as_view(), name="recommendation"),
    path("upload/", UploadFiles.as_view(), name="upload"),
    path("login/", loginView.as_view(), name = "login"),   
    path("logout/", logOutView.as_view(),name="logout")
]

