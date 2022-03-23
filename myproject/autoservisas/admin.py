from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.translation import gettext as _
from .models import CarModel, Car, Service, Order, OrderLine

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'engine', 'make_year')
    list_filter = ('cars__client', 'brand', 'model')
    search_fields = ('brand', 'model')


class CarAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'car_model', 'vin', 'client')
    list_filter = ('car_model', 'client')
    search_fields = ('licence_plate', 'vin')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('name',)
    search_fields = ('name',)


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    field = ('id', 'status', 'due_back')
    readonly_fields = ('id',)
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'car', 'total')
    list_filter = ('car__client', 'car__license_plate')
    search_fields = ('car__client',)
    inlines = (OrderLineInline,)

    
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'get_service_name', 'quantity', 'get_service_price')
    list_filter = ('order__car__client', 'order__car__license_plate', 'service__name')

    def get_service_name(self, obj):
        return obj.service.name
    get_service_name.short_description = _('Service')

    def get_service_price(self, obj):
        return obj.service.price
    get_service_price.short_description = _('Price')

# Register your models here.
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
