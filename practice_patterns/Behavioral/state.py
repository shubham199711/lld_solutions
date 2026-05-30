class OrderState:
    def next(self):
        pass

class Created(OrderState):
    def next(self):
        return Paid()

class Paid(OrderState):
    def next(self):
        return Shipped()

class Shipped(OrderState):
    def next(self):
        return Delivered()

class Delivered(OrderState):
    def next(self):
        return self

class Order:
    def __init__(self):
        self.state = Created()

    def advance(self):
        self.state = self.state.next()

order = Order()
print(type(order.state).__name__)

order.advance()
print(type(order.state).__name__)