from django.contrib import admin
from .models import Categoria, Producto, Empleado, Cliente, Venta, DetalleVenta
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(DetalleVenta)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'user')
