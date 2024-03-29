from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('reset-password/', views.reset_password_send_code, name='reset password send code'),
    path('reset-password-with-code/', views.reset_password_with_code, name='reset password with code'),
    path('profile/', views.profile_page, name='profile'),
    path('account-register/', views.register_page, name='register'),
    path('authenticate-email/', views.email_authentication, name='email authentication'),
    path('are-you-unesp/', views.are_you_unesp_page, name='are you unesp'),
    path('personal-data-reister/', views.personal_data_page, name='personal data'),
    path('personal-data-unesp-reister/', views.personal_data_unesp_page, name='personal data unesp'),
    path('presence/<str:lecture_name>', views.presence_page, name='presence page'),
    path('buy-subscription/', views.buy_subscription_page_placeholder, name='buy subscription page'),
    path('contact/', views.contact_page, name='contact page'),
    path('faq/', views.faq_page, name='faq page'),
    path('lecturers/', views.lecturers_page, name='lecturers page'),
    path('courses/', views.courses_page, name='courses page'),
    path('lectures/', views.lectures_page, name='lectures page'),
    path('lecturers/<int:id>/', views.lecturer_page, name='lecturer page'),
    path('tournament/', views.tournament_page, name='tournament page'),

    # Admin Only
    path('payment-confirmation/<str:cpf>', views.view_payment_confirmation, name='payment confirmation'),
    path('payment-confirmation-panel/', views.payment_confirmation_page, name='payment confirmation panel'),
]
