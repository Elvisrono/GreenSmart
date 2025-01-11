class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add(self, item_id, price, quantity=1):
        """Add an item to the cart or update the quantity if it already exists."""
        if item_id in self.cart:
            # If item exists, update the quantity
            self.cart[item_id]['quantity'] += quantity
        else:
            # If item does not exist, create a new entry for it
            self.cart[item_id] = {'price': price, 'quantity': quantity}
        self.save()

    def remove(self, item_id):
        """Remove an item from the cart."""
        if item_id in self.cart:
            del self.cart[item_id]  # Remove item from cart dictionary
            self.save()

    def save(self):
        """Save the cart back to the session."""
        self.session['cart'] = self.cart
        self.session.modified = True

    def get_total_price(self):
        """Recalculate total price."""
        total_price = 0
        for item_id, item_data in self.cart.items():
            total_price += item_data['price'] * item_data['quantity']
        return total_price

    def serialize(self):
        """Convert the cart to a format suitable for session storage."""
        return self.cart
