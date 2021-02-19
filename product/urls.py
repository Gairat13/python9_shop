from django.urls import path

from product.views import homepage, products_list, product_details


urlpatterns = [
    path('', homepage, name='index-page'),
    path('products/<slug:category_slug>/', products_list, name='products-list'),
    path('products/details/<int:product_id>/', product_details, name='product-details'),
]

