from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('account-register/', views.register_page, name='register'),
    path('are-you-unesp/', views.are_you_unesp_page, name='are you unesp'),
    path('personal-data-reister/', views.personal_data_page, name='personal data'),
    path('personal-data-unesp-reister/', views.personal_data_unesp_page, name='personal data unesp'),
    path('debug/', views.DEBUG_render_test, name='mesures'),
]
