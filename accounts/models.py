
from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from products.models import Product, ColorVariant, SizeVariant, Coupon
from home.models import ShippingAddress
from django.conf import settings
import os
# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, related_name="shipping_address", null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()
    
    def save(self, *args, **kwargs):
        # Check if the profile image is being updated and profile exists
        if self.pk:  # Only if profile exists
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.profile_image and old_profile.profile_image != self.profile_image:
                    old_image_path = os.path.join(settings.MEDIA_ROOT, old_profile.profile_image.path)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
            except Profile.DoesNotExist:
                # Profile does not exist, so nothing to do
                pass

        super(Profile, self).save(*args, **kwargs)



class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total_price = 0

        for cart_item in cart_items:
            total_price += cart_item.get_product_price()

        return total_price


    def get_cart_total_price_after_coupon(self):
        total = self.get_cart_total()

        if self.coupon and total >= self.coupon.minimum_amount:
            total -= self.coupon.discount_amount
                    
        return total



class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def get_product_price(self):
        price = self.product.price * self.quantity

        if self.color_variant:
            price += self.color_variant.price
            
        if self.size_variant:
            price += self.size_variant.price
        
        return price



