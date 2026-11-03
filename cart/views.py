from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from store.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    override = request.POST.get("override") == "1"

    if product.stock > 0:
        cart.add(product, quantity=quantity, override=override)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    return render(request, "cart/detail.html")

# Create your views here.
