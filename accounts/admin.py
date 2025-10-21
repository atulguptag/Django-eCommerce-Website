from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Profile, Cart, CartItem, Order, OrderItem

# Register your models here.


class ProfileAdminForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False, help_text="Upload an image file (will be converted to URL)")

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'profile_image': forms.URLInput(attrs={
                'placeholder': 'Enter image URL or upload a file below',
                'style': 'width: 100%;'
            })
        }


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ['user', 'is_email_verified', 'image_preview']
    readonly_fields = ['image_display']

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.profile_image)
        return "No Image"
    image_preview.short_description = 'Preview'

    def image_display(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="200" height="200" style="object-fit: cover; border-radius: 10px;" />', obj.profile_image)
        return "No Image"
    image_display.short_description = 'Profile Image'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
