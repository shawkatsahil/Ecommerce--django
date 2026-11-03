from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None
    q = request.GET.get("q", "").strip()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if q:
        products = products.filter(name__icontains=q)

    return render(request, "store/product_list.html", {
        "categories": categories,
        "products": products,
        "category": category,
        "q": q,
    })

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "store/product_list.html", {
        "categories": categories,
        "products": products,
        "category": category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "store/product_detail.html", {"product": product})

# Create your views here.
