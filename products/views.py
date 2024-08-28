import random
from .forms import ReviewForm
from django.urls import reverse
from django.contrib import messages
from accounts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from products.models import Product, SizeVariant, ProductReview, Wishlist
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    sorted_size_variants = product.size_variant.all().order_by('size_name')
    related_products = list(product.category.products.filter(parent=None).exclude(uid=product.uid))

    # Review product view
    review = None
    if request.user.is_authenticated:
        # Check if the user has already reviewed the product or not.
        try:
            review = ProductReview.objects.get(product=product, user=request.user)
        except ProductReview.DoesNotExist:
            review = None
    
    # Calculate the rating percentage
    rating_percentage = 0
    if product.reviews.exists():
        rating_percentage = (product.get_rating() / 5) * 100

    # Handle form submission
    if request.method == 'POST' and request.user.is_authenticated:
        if review:
            # If review exists, update it
            review_form = ReviewForm(request.POST, instance=review)
        else:
            # Otherwise, create a new review
            review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect('get_product', slug=slug)
    else:
        review_form = ReviewForm()
    
    # Related product view
    if len(related_products) >= 4:
        related_products = random.sample(related_products, 4)

    # Wishlist product to fetch, if the same item/product is present or not.
    in_wishlist = False  # Default value for anonymous users
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'sorted_size_variants': sorted_size_variants,
        'related_products': related_products,
        'review_form': review_form,
        'rating_percentage': rating_percentage,
        'in_wishlist': in_wishlist,
    }

    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product.get_product_price_by_size(size)
        context['selected_size'] = size
        context['updated_price'] = price

    return render(request, 'product/product.html', context=context)


# Add a product to Wishlist
@login_required
def add_to_wishlist(request, uid):
    variant = request.GET.get('size')
    if not variant:
        messages.error(request, 'Please select a size before adding to the wishlist!')
        return redirect(request.META.get('HTTP_REFERER'))
    
    product = get_object_or_404(Product, uid=uid)
    size_variant = get_object_or_404(SizeVariant, size_name=variant)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product, size_variant=size_variant)

    if created:
        messages.success(request, "Product added to Wishlist!")

    return redirect(reverse('wishlist'))


# Remove product from wishlist
@login_required
def remove_from_wishlist(request, uid):
    product = get_object_or_404(Product, uid=uid)
    size_variant_name = request.GET.get('size')
    
    if size_variant_name:
        size_variant = get_object_or_404(SizeVariant, size_name=size_variant_name)
        Wishlist.objects.filter(user=request.user, product=product, size_variant=size_variant).delete()
    else:
        Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.success(request, "Product removed from wishlist!")
    return redirect(reverse('wishlist'))


# Wishlist View
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'product/wishlist.html', 
                  {'wishlist_items': wishlist_items,}
                  )


# Move to cart functionality on wishlist page.
def move_to_cart(request, uid):
    product = get_object_or_404(Product, uid=uid)

    # Find the wishlist item with the corresponding size variant
    wishlist = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if not wishlist:
        messages.error(request, "Item not found in wishlist.")
        return redirect('wishlist')
    
    size_variant = wishlist.size_variant

    # Remove from wishlist
    wishlist.delete()

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)

    # Add the product to the cart with the size variant
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size_variant=size_variant)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product moved to cart successfully!")
    return redirect('cart')
