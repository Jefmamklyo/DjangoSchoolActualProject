#
#This is a project level urls.py
#
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path
import BSSSRemake.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BSSSRemake.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)