from django.urls import path
from .views import main_views, order_views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', main_views.dashboard_home, name='home'),
    
    # Order Management
    path('orders/', order_views.dashboard_order_list, name='order_list'),
    path('orders/<int:order_id>/', order_views.dashboard_order_detail, name='order_detail'),
]
