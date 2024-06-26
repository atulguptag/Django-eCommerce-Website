from django.urls import path
from accounts.views import login_page, register_page, activate_email_account, add_to_cart, cart, remove_cart, remove_coupon, success, user_logout

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', user_logout, name='logout'),
    path('activate/<email_token>/', activate_email_account, name="activate_email"),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('remove-cart/<uid>/', remove_cart, name="remove_cart"),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
    path('success/', success, name="success"),
]
