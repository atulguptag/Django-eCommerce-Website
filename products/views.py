from django.shortcuts import render, get_object_or_404
from products.models import Product
import random

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    sorted_size_variants = product.size_variant.all().order_by('size_name')
    related_products = list(product.category.products.filter(parent=None).exclude(uid=product.uid))

    print(len(related_products))
    
    if len(related_products) >= 4:
        related_products = random.sample(related_products, 4)

    context = {
        'product': product,
        'sorted_size_variants': sorted_size_variants,
        'related_products': related_products
    }

    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price

    return render(request, 'product/product.html', context=context)
