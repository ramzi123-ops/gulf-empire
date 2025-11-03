from django.urls import path
from apps.store.views import home, product_list, product_detail, add_review, gallery_list

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),
    path('gallery/', gallery_list, name='gallery'),
]
