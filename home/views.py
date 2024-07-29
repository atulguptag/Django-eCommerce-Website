from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.


def index(request):
    query = Product.objects.all()
    categories = Category.objects.all()
    selected_sort = request.GET.get('sort')
    selected_category = request.GET.get('category')

    if selected_category:
        query = query.filter(category__category_name=selected_category)

    if selected_sort:
        if selected_sort == 'newest':
            query = query.filter(newest_product=True).order_by('category_id')

        elif selected_sort == 'priceAsc':
            query = query.order_by('price')

        elif selected_sort == 'priceDesc':
            query = query.order_by('-price')

    context = {
        'products': query,
        'categories': categories,
        'selected_category': selected_category,
        'selected_sort': selected_sort,
    }
    return render(request, 'home/index.html', context)


def product_search(request):
    query = request.GET.get('q', '')

    if query:
        # Search for products that contain the query string in their product_name field
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(
            product_name__istartswith=query))
    else:
        products = Product.objects.none()

    context = {'query': query, 'products': products}
    return render(request, 'home/search.html', context)


def contact(request):
    message_name = ""
    if request.method == "POST":
        message_name = request.POST.get('message-name')
        message_lname = request.POST.get('message-lname')
        message_email = request.POST.get('message-email')
        message = request.POST.get('message')

        subject = f"Message from {message_name} {message_lname}"
        email_from = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            email_from,
            [message_email],
            fail_silently=False,
        )

        messages.success(request, 'Thank you for your message. We will get back to you soon..')
        return HttpResponseRedirect(request.path_info)

    context = {'message_name': message_name}
    return render(request, 'home/contact.html', context)

def about(request):
    return render(request, 'home/about.html')