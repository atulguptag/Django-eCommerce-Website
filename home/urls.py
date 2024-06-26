from django.urls import path
from home.views import index, product_search

urlpatterns = [
    path('', index, name="index"),
    path('search/', product_search, name='product_search'),
]
