from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html
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


class OrderInstanceInline(admin.TabularInline):
    model = OrderInstance
    field = ('id', 'status', 'due_back')
    readonly_fields = ('id',)
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'created_at', 'car' , 'get_services', 'total')
    list_filter = ('client', 'service__name')
    search_fields = ('client', 'service')
    inlines = (OrderInstanceInline,)

    def get_services(self, obj):
        services = ', '.join(service.name for service in obj.service.all()[:2])
        if obj.service.count() > 2:
            return ', '.join([services, '...'])
        return services
    get_services.short_description = _('Services')


class OrderInstanceAdmin(admin.ModelAdmin):
    list_display =('get_short_id_link', 'get_client', 'status', 'due_back', 'is_overdue')
    list_filter = ('status',)
    search_field = ('id', 'status', 'is_overdue')
    readonly_fields = ('id',)

    def get_short_id_link(self,obj):
        return format_html('<a href="{}">...{}</a>', reverse_lazy('admin:autoservisas_orderinstance_change', args=[obj.id]), str(obj.id)[:-12])

    def get_client(self,obj):
        return obj.order.client


# Register your models here.
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInstance, OrderInstanceAdmin)
