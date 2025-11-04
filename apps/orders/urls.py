from django.urls import path
from apps.orders.views import add_to_cart, update_cart_item, remove_from_cart, view_cart
from apps.orders.views.checkout_views import checkout
from apps.orders.views.order_views import order_detail, order_list

app_name = 'orders'

urlpatterns = [
    path('cart/', view_cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    
    # Order management
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
]
