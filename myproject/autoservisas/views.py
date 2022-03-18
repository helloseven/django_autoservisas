from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .models import Car, Service, Order, OrderInstance


class OrderListView(generic.ListView):
    model = Order
    template_name = 'autoservisas/all_orders.html'
    context_object_name = 'orders'
    paginate_by = 2    
    
    def get_queryset(self):
        return super().get_queryset()

   
class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'autoservisas/order_detail.html'
    context_object_name = 'order'

    def get_success_url(self):
        return reverse_lazy('autoservisas:order-detail', kwargs={'pk' : self.object.id})

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['order'] = self.object
    #     return context

def index(request):
    num_services = Service.objects.count()
    num_instances_completed = OrderInstance.objects.filter(status__exact=2).count()
    num_cars = Car.objects.count()

    context = {
        'num_services' : num_services,
        'num_instances_completed' : num_instances_completed,
        'num_cars' : num_cars
    }
    return render(request, 'autoservisas/index.html', context=context)


def cars(request):
    all_cars = Car.objects.all()
    return render(request, 'autoservisas/all_cars.html', {'cars':all_cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'autoservisas/car_detail.html', {'car': car})


