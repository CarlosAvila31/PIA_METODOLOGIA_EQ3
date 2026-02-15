from django.contrib import admin
from .models import Categoria, Producto, Empleado, Cliente, Venta, DetalleVenta, Caja, Proveedor, Compra, DetalleCompra, CuentaPorPagar
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Caja)
admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
admin.site.register(CuentaPorPagar)
