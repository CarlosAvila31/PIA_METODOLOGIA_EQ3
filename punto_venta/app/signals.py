from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetallesVentas

@receiver(post_save, sender=DetallesVentas)
@receiver(post_delete, sender=DetallesVentas)
def actualizar_total_venta(sender, instance, **kwargs):
    venta = instance.venta

    total = sum(detalle.subtotal for detalle in venta.detalles.all())

    venta.total = total
    venta.save()