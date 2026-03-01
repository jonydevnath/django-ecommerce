from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('search/', views.search_products, name='search'),
    path('analytics/', views.category_analytics, name='analytics'),
    path('add/', views.add_product, name='add_product'),
    path('low-stock/', views.low_stock_alert, name='low_stock'),
]
