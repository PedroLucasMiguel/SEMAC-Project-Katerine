from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('Zlp6LJQ8D8/', admin.site.urls),
    path('admin/', views.adminCheck),
    path('', include('usermanager.urls')),
]
