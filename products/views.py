from django.shortcuts import render, get_object_or_404
from products.models import Product

def get_product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        sorted_size_variants = product.size_variant.all().order_by('size_name')
        context = {
            'product': product,
            'sorted_size_variants': sorted_size_variants
        }

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'product/product.html', context=context)
    except Exception as e:
        print(e)
