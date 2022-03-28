from django.urls import path

from . import views

app_name = 'autoservisas'
urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car_detail, name='car-detail'),
    path('cars/search/', views.search_cars, name='car-search'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/create', views.OrderCreateView.as_view(), name='create-order'),  
    path('orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='update-order'),  
    path('orders/<int:pk>/delete', views.OrderDeleteView.as_view(), name='delete-order'),  
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),  
]
