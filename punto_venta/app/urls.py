from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView


urlpatterns = [
    path('', CustomLoginView.as_view(), name='inicio'), 
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('venta/', views.listar_productos, name='venta'),
    path('listar_empleado/', views.listar_empleado, name='listar_empleado'),
    path('listado_ventas/', views.listado_ventas, name='listado_ventas'),
    path('eliminar/<int:id>/', views.eliminar_venta, name='eliminar'),
]