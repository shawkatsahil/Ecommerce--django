from django.contrib import messages
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


def _mark_order_paid(order):
    """Mark the order as paid and lower the stock. Safe to call twice."""
    with transaction.atomic():
        order = Order.objects.select_for_update().get(pk=order.pk)
        if order.status != "pending":
            return False
        order.status = "paid"
        order.save(update_fields=["status"])
        for item in order.items.select_related("product"):
            product = item.product
            product.stock = max(0, product.stock - item.quantity)
            product.save(update_fields=["stock"])
    return True


@login_required
def payment_start(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")

    if request.method == "POST":
        card = request.POST.get("card_number", "").replace(" ", "")
        if card == "4242424242424242":
            _mark_order_paid(order)
            messages.success(request, "Payment received. Thank you for your order!")
            return redirect("orders:order_detail", order_id=order.id)
        messages.error(request, "Card declined. Use the test card 4242 4242 4242 4242.")

    return render(request, "orders/payment.html", {"order": order})
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders/order_list.html", {"orders": orders})

# Create your views here.
