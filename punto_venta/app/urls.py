from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView


urlpatterns = [
    path('', CustomLoginView.as_view(), name='inicio'), 
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('venta/', views.listar_productos, name='venta'),
    path('listado_ventas/', views.listado_ventas, name='listado_ventas'),
    path('eliminar/<int:id>/', views.eliminar_venta, name='eliminar'),
    path('guardar-venta/', views.guardar_venta, name='guardar_venta'),
    path('informes/', views.dashboard, name='dashboard'),
    path('analytics/ventas-dia/', views.ventas_por_dia),
    path('analytics/productos-top/', views.productos_top),
    path('analytics/resumen/', views.resumen),
]