import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Empleado, Cliente, Venta, DetalleVenta
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from django.utils import timezone 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db import models



# Create your views here.


class RoleLoginForm(AuthenticationForm):
    role = forms.ChoiceField(
        choices=[('admin', 'Administrador'), ('empleado', 'Empleado')],
        label='Tipo de usuario'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'id': 'id_role'})

def is_admin(user):
    return user.is_superuser

def is_empleado(user):
    return user.groups.filter(name='Empleados').exists()

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})



class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = RoleLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        
        if user.is_superuser:
            return redirect('venta')
        elif is_empleado(user):
            return redirect('venta')
        return response


def listado_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'listado_ventas.html', {'ventas': ventas})




def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    venta.delete()
    return redirect('listado_ventas')


@login_required
def guardar_venta(request):
    if request.method == "POST":

        data = json.loads(request.body)

        carrito = data.get("carrito", [])
        metodo_pago = data.get("metodo_pago")
        nombre = data.get("nombre")
        apellido = data.get("apellido")

        # ==========================
        # EMPLEADO (DESDE USER)
        # ==========================
        empleado = request.user.empleado

        # ==========================
        # CLIENTE (OPCIONAL)
        # ==========================
        cliente = None
        if nombre:
            cliente = Cliente.objects.create(
                nombre=nombre,
                primer_apellido=apellido
            )

        # ==========================
        # CREAR VENTA
        # ==========================
        venta = Venta.objects.create(
            fecha_hora=timezone.now(),
            metodo_pago=metodo_pago,
            empleado=empleado,
            cliente=cliente
        )

        total = 0

        # ==========================
        # DETALLE VENTA
        # ==========================
        for item in carrito:

            producto = Producto.objects.get(id=item["id"])

            detalle = DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item["cantidad"]
            )

            total += detalle.subtotal

        # ==========================
        # ACTUALIZAR TOTAL
        # ==========================
        venta.total = total
        venta.save()

        return JsonResponse({"status": "ok"})