from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView


urlpatterns = [
    path('', views.inicio, name='inicio'), 
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('listar/', views.listar_reservaciones, name='listar'),
]