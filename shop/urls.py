from django.urls import path, include
from . import views
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('product_details/', views.product_details, name='product_detail'),
    path('shop/', views.shop, name='shop'),
    path('contact/',views.contact, name='contact'),
    path('product-details-affiliate/',views.product_affiliate, name='affiliate'),
    path('product-details-group/',views.product_group, name='group'),
    path('product-details-variable/',views.product_variable, name='variable'),
    path('applications/', views.ApplicationsView.as_view(), name='applications'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]