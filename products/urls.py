from django.urls import path
from products.views import get_product, wishlist_view, add_to_wishlist, move_to_cart, remove_from_wishlist

urlpatterns = [
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<uid>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/move_to_cart/<uid>/', move_to_cart, name='move_to_cart'),
    path('wishlist/remove/<uid>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('<slug>/', get_product, name='get_product'),
]
