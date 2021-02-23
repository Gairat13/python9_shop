from django.urls import path

from product.views import HomePageView, ProductsListView, ProductDetails


urlpatterns = [
    path('', HomePageView.as_view(), name='index-page'),
    path('products/<slug:category_slug>/', ProductsListView.as_view(), name='products-list'),
    path('products/details/<int:pk>/', ProductDetails.as_view(), name='product-details'),
]

