from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('account-register/', views.register_page, name='register'),
    path('authenticate-email/', views.email_authentication, name='email authentication'),
    path('are-you-unesp/', views.are_you_unesp_page, name='are you unesp'),
    path('personal-data-reister/', views.personal_data_page, name='personal data'),
    path('personal-data-unesp-reister/', views.personal_data_unesp_page, name='personal data unesp'),
    path('presence/<str:lecture_name>', views.presence_page, name='presence page'),
    path('buy-subscription/', views.buy_subscription_page, name='buy subscription page'),
    path('contact/', views.contact_page, name='contact page'),

    path('payment-confirmation/<str:cpf>', views.view_payment_confirmation, name='payment confirmation'),

    path('test-smtp/', views.DEBUG_test_smtp, name='SMTP'),
    path('debug/', views.DEBUG_render_test, name='mesures'),
]
