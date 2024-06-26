from django.shortcuts import render
from products.models import Product
from django.db.models import Q

# Create your views here.


def index(request):
    context = {'products': Product.objects.all()}
    return render(request, 'home/index.html', context)


def product_search(request):
    query = request.GET.get('q', '')
    products = []

    if query:
        # Search for products that contain the query string in their name or description
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'home/search.html', context) 
