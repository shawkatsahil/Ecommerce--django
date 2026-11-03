from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["product"].price,
                        quantity=item["quantity"],
                    )
            cart.clear()
            return redirect("orders:order_detail", order_id=order.id)
    else:
        form = OrderCreateForm(initial={"email": request.user.email})

    return render(request, "orders/checkout.html", {"form": form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})

# Create your views here.
