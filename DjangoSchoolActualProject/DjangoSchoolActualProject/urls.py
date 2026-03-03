from django.urls import include, path
import BSSSRemake.views

urlpatterns = [
    path('', include('BSSSRemake.urls'))
]