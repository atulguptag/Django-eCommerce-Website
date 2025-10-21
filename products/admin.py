from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import *

# Register your models here.


class CategoryAdminForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False, help_text="Upload an image file (will be converted to URL)")

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category_image': forms.URLInput(attrs={
                'placeholder': 'Enter image URL or upload a file below',
                'style': 'width: 100%;'
            })
        }


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ['category_name', 'image_preview']

    def image_preview(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.category_image)
        return "No Image"
    image_preview.short_description = 'Preview'


class ProductImageAdminForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False, help_text="Upload an image file (will be converted to URL)")

    class Meta:
        model = ProductImage
        fields = '__all__'
        widgets = {
            'image_url': forms.URLInput(attrs={
                'placeholder': 'Enter image URL or upload a file below',
                'style': 'width: 100%;'
            })
        }


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    form = ProductImageAdminForm
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="200" style="object-fit: contain;" />', obj.image_url)
        return "No Image"
    image_preview.short_description = 'Preview'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price']
    inlines = [ProductImageAdmin]


class ProductImageStandaloneAdmin(admin.ModelAdmin):
    form = ProductImageAdminForm
    list_display = ['product', 'image_thumbnail']
    readonly_fields = ['img_preview']

    def image_thumbnail(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image_url)
        return "No Image"
    image_thumbnail.short_description = 'Thumbnail'


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']
    model = ColorVariant


@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price', 'order']
    model = SizeVariant


admin.site.register(Category, CategoryAdmin)
admin.site.register(Coupon)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageStandaloneAdmin)
admin.site.register(ProductReview)
