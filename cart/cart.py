CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart  # looks like {"3": 2, "5": 1}  (product id: quantity)

    def add(self, product, quantity=1, override=False):
        pid = str(product.id)
        if override:
            self.cart[pid] = quantity
        else:
            self.cart[pid] = self.cart.get(pid, 0) + quantity
        # never more than we have in stock, never less than 1
        self.cart[pid] = max(1, min(self.cart[pid], product.stock))
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def __iter__(self):
        from store.models import Product
        products = Product.objects.filter(id__in=self.cart.keys())
        for product in products:
            quantity = self.cart[str(product.id)]
            yield {
                "product": product,
                "quantity": quantity,
                "total_price": product.price * quantity,
            }

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        return sum(item["total_price"] for item in self)