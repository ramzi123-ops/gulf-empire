from django.urls import path
from apps.store.views import product_list, product_detail, add_review

app_name = 'store'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),
]
