from django.urls import path
from apps.store.views import home, product_list, product_detail, add_review, gallery_list
from apps.store.views.page_views import about_view, contact_view, gallery_view

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('products/', product_list, name='product_list'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', add_review, name='add_review'),
    
    # Static Pages
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('gallery/', gallery_list, name='gallery'),
]
