from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/', views.profilepage, name='profile'),
    path('account-register/', views.registerpage, name='register'),
    path('debug/', views.DEBUG_render_test, name='mesures'),
]
