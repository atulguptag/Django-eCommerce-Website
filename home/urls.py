from django.urls import path
from home.views import index, product_search, contact, about

urlpatterns = [
    path('', index, name="index"),
    path('search/', product_search, name='product_search'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
]
