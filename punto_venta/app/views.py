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
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate



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



def dashboard(request):
    return render(request, 'dashboard.html')



def resumen(request):
    total = Venta.objects.aggregate(total=Sum('total'))['total'] or 0
    promedio = Venta.objects.aggregate(promedio=Avg('total'))['promedio'] or 0

    producto_top = (
        DetalleVenta.objects
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
        .first()
    )

    return JsonResponse({
        "total": round(total, 2),
        "promedio": round(promedio, 2),
        "producto_top": producto_top['producto__nombre'] if producto_top else "-"
    })




def ventas_por_dia(request):
    ventas = (
        Venta.objects
        .annotate(fecha_dia=TruncDate('fecha_hora'))
        .values('fecha_dia')
        .annotate(total=Sum('total'))
        .order_by('fecha_dia')
    )

    data = {
        "labels": [v["fecha_dia"].strftime("%Y-%m-%d") for v in ventas],
        "data": [v["total"] for v in ventas]
    }

    return JsonResponse(data)



def productos_top(request):
    productos = (
        DetalleVenta.objects
        .values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:5]
    )

    data = {
        "labels": [p["producto__nombre"] for p in productos],
        "data": [p["total_vendido"] for p in productos]
    }

    return JsonResponse(data)