from django.urls import path
from apps.store.views import product_list, product_detail

app_name = 'store'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
]