from django.db import models


# Create your models here.
class Venta(models.Model):
    producto = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        db_table = 'ventas'

    def __str__(self):
        return self.producto
