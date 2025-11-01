from django.urls import path
from apps.orders.views import add_to_cart, update_cart_item, remove_from_cart, view_cart
from apps.orders.views.checkout_views import checkout

app_name = 'orders'

urlpatterns = [
    path('cart/', view_cart, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
]
