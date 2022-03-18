from django.contrib import admin
from django.utils.translation import gettext as _
from .models import CarModel, Car, Service, Order, OrderInstance

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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'car' , 'get_services', 'total')
    list_filter = ('car', 'service__name')
    search_fields = ('car', 'service')

    def get_services(self, obj):
        services = ', '.join(service.name for service in obj.service.all()[:2])
        if obj.service.count() > 2:
            return ', '.join([services, '...'])
        return services
    get_services.short_description = _('Services')


class OrderInstanceAdmin(admin.ModelAdmin):
    list_display =('id', 'order_id', 'status')
    list_filter = ('status', 'order__service__name')
    search_field = ('status',)


# Register your models here.
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInstance, OrderInstanceAdmin)
