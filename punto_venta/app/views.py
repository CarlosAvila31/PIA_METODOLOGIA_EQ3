from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Empleado, Cliente, Venta, DetalleVenta, Caja, Proveedor, Compra, DetalleCompra, CuentaPorPagar
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime, timedelta
from django.utils import timezone 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.db import models



# Create your views here.
def inicio(request):
    return render(request, 'login.html')


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
@user_passes_test(is_admin)
def listar_reservaciones(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

@login_required
@user_passes_test(is_empleado)
def listar_empleado(request):
    productos = Producto.objects.all()
    return render(request, 'listar_empleado.html', {'productos': productos})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = RoleLoginForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        
        if user.is_superuser:
            return redirect('listar')
        elif is_empleado(user):
            return redirect('listar_empleado')
        return response


def listado_ventas(request):
    productos = Producto.objects.all()
    return render(request, 'listado_ventas.html', )


def listar_empleado(request):
    return render(request, 'listar_empleado.html')