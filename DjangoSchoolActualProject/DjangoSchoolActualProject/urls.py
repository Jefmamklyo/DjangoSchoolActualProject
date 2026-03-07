#
#This is a project level urls.py
#
from django.contrib import admin

from django.urls import include, path
import BSSSRemake.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BSSSRemake.urls'))
]