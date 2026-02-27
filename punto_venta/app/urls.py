from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView


urlpatterns = [
    path('', CustomLoginView.as_view(), name='inicio'), 
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('listar/', views.listar_reservaciones, name='listar'),
    path('listar_empleado/', views.listar_empleado, name='listar_empleado'),
    path('listado_ventas/', views.listado_ventas, name='listado_ventas'),
]