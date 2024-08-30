from django.urls import path
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    #User view urls with login, register, logout, and email activation.
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('logout/', user_logout, name='logout'),
    path('activate/<email_token>/', activate_email_account, name="activate_email"),
    
    #Profile management urls with profile, change-password, and shipping-address
    path('profile/<str:username>/', profile_view, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('shipping-address/', update_shipping_address, name='shipping-address'),
    
    #Passoword reset urls with django default view.
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
        
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    #Cart functionality with add-to-cart, update-cart, remove-cart, and remove-coupon urls.
    path('cart/', cart, name="cart"),
    path('add-to-cart/<uid>/', add_to_cart, name="add_to_cart"),
    path('update_cart_item/', update_cart_item, name='update_cart_item'),
    path('remove-cart/<uid>/', remove_cart, name="remove_cart"),
    path('remove-coupon/<cart_id>/', remove_coupon, name="remove_coupon"),
    
    #Success url after payment is done.
    path('success/', success, name="success"),
    
    #Order history and details urls
    path('order-history/', order_history, name='order_history'),
    path('order-details/<str:order_id>/', order_details, name='order_details'),
    path('order-details/<str:order_id>/download/', download_invoice, name='download_invoice'),

    #Delete user account url
    path('delete-account/', delete_account, name='delete_account'),
]
