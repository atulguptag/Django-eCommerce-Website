from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', user_logout, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('shipping-address/', update_shipping_address, name='shipping-address'),
    path('activate/<email_token>/', activate_email_account, name="activate_email"),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
        
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('cart/', cart, name="cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('update_cart_item/', update_cart_item, name='update_cart_item'),
    path('remove-cart/<uid>/', remove_cart, name="remove_cart"),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
    path('success/', success, name="success"),
    path('success/download_invoice/<razorpay_order_id>/', download_invoice, name='download_invoice'),
]
