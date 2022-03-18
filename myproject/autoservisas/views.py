from django.db.models import Q
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
    paginator = Paginator(Car.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars' : paged_cars,
        'cars_count' : Car.objects.count()
    }
    return render(request, 'autoservisas/all_cars.html', context=context)


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'autoservisas/car_detail.html', {'car': car})


def search_cars(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(client__username__icontains=query) |
        Q(car_model__model__icontains=query) |
        Q(license_plate__icontains=query) |
        Q(vin__icontains=query)
    )
    context = {
        'cars' : search_results,
        'query' : query,
    }
    return render(request, 'autoservisas/search_cars.html', context=context)
