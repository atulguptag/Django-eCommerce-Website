from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from products.models import *
from accounts.models import Profile, Cart, CartItem
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required

import uuid
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found!')
            return HttpResponseRedirect(request.path_info)

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Account not verified!')
            return HttpResponseRedirect(request.path_info)

        # then authenticate user
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, 'Login Successfull.')
            return redirect('/')

        messages.warning(request, 'Invalid credentials.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username)

        if user_obj.exists():
            messages.warning(request, 'Account already exists.')
            return HttpResponseRedirect(request.path_info)

        # if user not registered
        user_obj = User.objects.create(
            first_name=first_name, last_name=last_name, email=email, username=username)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent to your mail.')
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged Out Successfully!")
    return redirect('index')


def activate_email_account(request, email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Account verification successful.')
        return redirect('login')
    except Exception as e:
        return HttpResponse('Invalid email token.')





@login_required
def add_to_cart(request, uid):
    try:
        variant = request.GET.get('variant')
        color = request.GET.get('color')
        product = get_object_or_404(Product, uid=uid)

        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        cart_item = CartItem.objects.create(cart=cart, product=product)

        if variant:
            size_variant = get_object_or_404(SizeVariant, size_name=variant)
            cart_item.size_variant = size_variant

        if color:
            color_variant = get_object_or_404(ColorVariant, color_name=color)
            cart_item.color_variant = color_variant

        cart_item.save()

        messages.success(request, 'Item added to cart successfully.')
        
    except Exception as e:
        print(e)
        messages.error(request, 'Error adding item to cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart(request):
    cart_obj = None
    payment = None
    
    try:
        cart_obj = Cart.objects.get(is_paid = False, user = request.user)

    except Cart.DoesNotExist:
        cart_obj = None

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__exact=coupon).first()

        if not coupon_obj:
            messages.warning(request, 'Invalid coupon code.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj and cart_obj.coupon:
            messages.warning(request, 'Coupon already exists.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj and coupon_obj.is_expired:
            messages.warning(request, 'Coupon code expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj and coupon_obj and cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(
                request, f'Amount should be greater than {coupon_obj.minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj and coupon_obj:
            cart_obj.coupon = coupon_obj
            cart_obj.save()
            messages.success(request, 'Coupon applied successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if cart_obj:
        
        cart_total_in_paise = int(cart_obj.get_cart_total_price_after_coupon() * 100)
        
        if cart_total_in_paise < 100:
            messages.warning(request, 'Total amount in cart is less than the minimum required amount (1.00 INR).')
            return redirect('index') 
        
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        payment = client.order.create({'amount': cart_total_in_paise, 'currency': 'INR', 'payment_capture': 1})
        cart_obj.razorpay_order_id = payment['id']
        cart_obj.save()

        print("**********************")
        print(payment)
        print("**********************")


    context = {'cart': cart_obj, 'payment': payment}
    return render(request, 'accounts/cart.html', context)


def remove_cart(request, uid):
    try:
        cart_item = get_object_or_404(CartItem, uid=uid)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')

    except Exception as e:
        print(e)
        messages.error(request, 'Error removing item from cart.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()

    messages.success(request, 'Coupon Removed.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def success(request):
    order_id = request.GET.get('order_id')
    # cart = Cart.objects.get(razorpay_order_id = order_id)
    cart = get_object_or_404(Cart, razorpay_order_id = order_id)
    cart.is_paid = True
    cart.save()

    context = {'order_id': order_id}
    return render(request, 'payment_success/payment_success.html', context)


# HTML to PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)

    file_name = uuid.uuid4()

    try:
        with open(str(settings.BASE_DIR) + f"/public/media/{file_name}.pdf", 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)

    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    
    return file_name, True
    

def download_invoice(request, razorpay_order_id):
    order = get_object_or_404(Cart, razorpay_order_id=razorpay_order_id)
    context = {
        'order': order,
        'data': {
            'order_date': order.created_at,
            'name': order.user.get_full_name(),
            'user_email': order.user.email
        }
    }
    pdf = render_to_pdf('pdfs/invoice.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{razorpay_order_id}.pdf"'
    return response
