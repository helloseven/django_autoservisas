from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .models import Car, Service, Order, OrderLine
from .forms import OrderCreateForm

def index(request):
    num_services = Service.objects.count()
    num_orders = Order.objects.count()
    num_orderlines_created = OrderLine.objects.count()
    num_cars = Car.objects.count()
    num_visits = int(request.session.get('num_visits', 0)) + 1
    request.session['num_visits'] = num_visits

    context = {
        'num_services' : num_services,
        'num_orders' : num_orders,
        'num_orderlines_created' : num_orderlines_created,
        'num_cars' : num_cars,
        'num_visits' : num_visits,
    }
    return render(request, 'autoservisas/index.html', context=context)


def cars(request):
    if request.user.is_superuser or request.user.is_staff:
        paginator = Paginator(Car.objects.all(), 5)
    else:
        paginator = Paginator(Car.objects.filter(client_id=request.user), 5)
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


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'autoservisas/all_orders.html'
    queryset = Order.objects.all()
    context_object_name = 'orders'
    paginate_by = 5    

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = Order.objects.all()
        else:
            queryset = super().get_queryset().filter(car__client_id=self.request.user)
        return queryset

    
class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'autoservisas/order_detail.html'
    context_object_name = 'order'

    def get_success_url(self):
        return reverse_lazy('autoservisas:order-detail', kwargs={'pk' : self.object.id})


class OrderCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = reverse_lazy('autoservisas:orders')
    template_name = 'autoservisas/create_order.html'

    def test_func(self):
        return not self.request.user.is_staff or not self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


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
