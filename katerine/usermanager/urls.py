from django.urls import path
from . import views

urlpatterns = [
    path('', views.DEBUG_render_test, name='debug_render_test'),
    path('thread', views.DEBUG_testing_mesures, name='mesures'),
]
