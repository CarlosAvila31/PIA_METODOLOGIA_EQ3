from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Empleado, Cliente, Venta, DetalleVenta, Caja, Proveedor, Compra, DetalleCompra, CuentaPorPagar


# Create your views here.
def inicio(request):
    return render(request, 'index.html')