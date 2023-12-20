class Cart:
    def __init__(self, cart_id=None, customer_id=None, product_id=None, quantity=None):
        self.cart_id = cart_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    def get_cart_id(self):
        return self.cart_id

    def set_cart_id(self, cart_id):
        self.cart_id = cart_id

    def get_customer_id(self):
        return self.customer_id

    def set_customer_id(self, customer_id):
        self.customer_id = customer_id

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, product_id):
        self.product_id = product_id

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity
