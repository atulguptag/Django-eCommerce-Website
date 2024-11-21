from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

    page = request.GET.get('page', 1)
    paginator = Paginator(query, 20)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except Exception as e:
        print(e)

    context = {
        'products': products,
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
    try:
        if request.method == "POST":
            message_name = request.POST.get('message-name')
            message_lname = request.POST.get('message-lname')
            message_email = request.POST.get('message-email')
            message = request.POST.get('message')
            validate_email(message_email)

            subject = f"Message from {message_name} {message_lname} - {message_email}"
            email_from = settings.DEFAULT_FROM_EMAIL

            send_mail(
                subject,
                message,
                message_email,
                [email_from],
                fail_silently=False,
            )

            messages.success(
                request, f'Hii, {message_name}! Thank you for your message. We will get back to you soon...')
            return HttpResponseRedirect(request.path_info)

        return render(request, 'home/contact.html')

    except Exception:
        messages.warning(request, 'Invalid Email Address!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'home/about.html')


def terms_and_conditions(request):
    return render(request, 'home/terms_and_conditions.html')


def privacy_policy(request):
    return render(request, 'home/privacy_policy.html')
