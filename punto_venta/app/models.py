from django.db import models
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User


# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre




class Producto(models.Model):
    nombre = models.CharField(max_length=70)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT) #el PORTECT evita borrar una categoría si tiene productos aja baraja.

    def __str__(self):
        return self.nombre
    



class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    nombre = models.CharField(max_length=45)
    primer_apellido = models.CharField(max_length=45)
    segundo_apellido = models.CharField(max_length=45, null=True, blank=True)
    rfc = models.CharField(max_length=13)

    def __str__(self):
        if self.user:
            return f"{self.nombre} ({self.user.username})"
        return self.nombre
    




class Cliente(models.Model):
    nombre = models.CharField(max_length=45)
    primer_apellido = models.CharField(max_length=45)
    segundo_apellido = models.CharField(max_length=45, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    descripcion = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.nombre
    



class Venta(models.Model):
    fecha_hora = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) #TOTAL A PAGAR
    metodo_pago = models.CharField(max_length=45) #Efectivo, Tarjeta, etc.

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )



    def __str__(self):
        return f"Venta #{self.id}"
    


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # Tomar automáticamente el precio del producto
        if self.producto:
            self.precio_unitario = self.producto.precio_venta

        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de venta {self.venta.id}"



class Caja(models.Model):
    dinero_en_caja = models.DecimalField(max_digits=10, decimal_places=2)

    venta = models.ForeignKey(
        Venta,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )




class Proveedor(models.Model):
    nombre = models.CharField(max_length=70)
    rfc = models.CharField(max_length=13)
    telefono = models.CharField(max_length=10)
    email = models.EmailField()
    direccion = models.CharField(max_length=70)

    def __str__(self):
        return self.nombre





class Compra(models.Model):
    fecha_registro = models.DateField(auto_now_add=True)
    forma_pago = models.CharField(max_length=45)
    fecha_plazo_credito = models.DateField(null=True, blank=True)
    subtotal_compra = models.DecimalField(max_digits=10, decimal_places=2)

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT
    )

    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"Compra #{self.id}"





class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveSmallIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)





class CuentaPorPagar(models.Model):

    estado = models.CharField(max_length=20) #Igual aqui tenia pensado que fuera algo como "Pendiente", "Pagada", etc. para llevar un control de las cuentas por pagar pero no se que opinen.
    abono = models.DecimalField(max_digits=10, decimal_places=2)
    detalles = models.CharField(max_length=100)

    saldo = models.DecimalField(max_digits=10, decimal_places=2)

    compra = models.ForeignKey(
        Compra,
        on_delete=models.PROTECT
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT
    )

    fecha_compra = models.DateField()
    fecha_plazo_credito = models.DateField()

    def __str__(self):
        return f"Cuenta por pagar #{self.id}"
