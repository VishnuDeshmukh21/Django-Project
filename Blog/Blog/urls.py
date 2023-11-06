
from django.contrib import admin
from django.urls import path,include

from django.http import JsonResponse
from base import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('accounts/',include('users.urls')),
    
]