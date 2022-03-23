from django.conf import settings 
from django.db import models
from decimal import Decimal
from datetime import date
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tinymce.models import HTMLField
import uuid


class CarModel(models.Model):
    brand = models.CharField(_('Brand'), max_length=200, db_index=True)
    model = models.CharField(_('Model'), max_length=200, db_index=True)
    engine = models.CharField(_('Engine'), max_length=200)
    make_year = models.PositiveIntegerField(_('Make Year'))

    class Meta:
        ordering = ['brand', 'model']
        verbose_name = _('Car Model')
        verbose_name_plural = _('Car Models')

    def __str__(self) -> str:
        return f'{self.brand} {self.model} {self.make_year}'


class Car(models.Model):
    license_plate = models.CharField(_('License Plate'), max_length=200, db_index=True)
    car_model = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True, related_name='cars')
    vin = models.CharField(_('VIN code'), max_length=200)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    description = HTMLField(_('Description'), max_length=1000, null=True, help_text=_('Short description of the car'))
    image = models.ImageField(_('Image'), upload_to='img', null=True, blank=True)

    class Meta:
        ordering = ['client', 'car_model_id']
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self) -> str:
        return f'{self.car_model.brand} {self.car_model.model} {self.license_plate} {self.client}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=200, help_text='Name of a service provided.', db_index=True)
    price = models.DecimalField(_('Price'), max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], db_index=True)
    
    class Meta:
        ordering = ['name', 'price']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self) -> str:
        return f'{self.name} {self.price}$'


class Order(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    due_back = models.DateField(_('Due back'), null=True, blank=True, db_index=True)

    class Meta:
        ordering = ['created_at', 'car']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self) -> str:
        return f'{self.car}'

    @property
    def total(self):
        sum = 0
        for line in self.order_lines.all():
            sum += line.service.price * line.quantity
        return sum
        


class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, 
        null=False, 
        on_delete=models.CASCADE, 
        verbose_name=_('Order'),
        related_name='order_lines'
    )
    service = models.ForeignKey(Service,
        null=False,
        on_delete=models.CASCADE,
        verbose_name=_('Service'),
        related_name='order_lines'
        )

    quantity = models.PositiveIntegerField(_('Quantity'), null=False, default=1)

    def __str__(self):
        return f'{self.id} {self.service.name} {self.quantity} {self.order.total}'



    





    


