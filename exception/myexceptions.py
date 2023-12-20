class CustomerNotFoundException(Exception):
    def __init__(self, msg="CustomerNotFoundException"):
        self.msg = msg
        super().__init__(self.msg)


class ProductNotFoundException(Exception):
    def __init__(self, msg="ProductNotFoundException"):
        self.msg = msg
        super().__init__(self.msg)


class OrderNotFoundException(Exception):
    def __init__(self, msg="OrderNotFoundException"):
        self.msg = msg
        super().__init__(self.msg)
        