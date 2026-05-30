from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, price):
        pass

class RegularPricing(PricingStrategy):
    def calculate(self, price):
        return price

class FestivalPricing(PricingStrategy):
    def calculate(self, price):
        return price * 0.8

class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy

    def total(self, amount):
        return self.strategy.calculate(amount)

checkout = Checkout(FestivalPricing())
print(checkout.total(1000))