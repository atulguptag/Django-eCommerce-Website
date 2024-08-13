from django.urls import path
from home.views import *

urlpatterns = [
    path('', index, name="index"),
    path('search/', product_search, name='product_search'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('shipping-address/', update_shipping_address, name='shipping-address'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
]
