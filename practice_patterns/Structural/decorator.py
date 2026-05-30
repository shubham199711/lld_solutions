from abc import ABC, abstractmethod


class Coffee(ABC):

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_price(self):
        pass


class Espresso(Coffee):

    def get_description(self):
        return "Espresso"

    def get_price(self):
        return 100


class AddOn(Coffee):

    def __init__(self, coffee: Coffee):
        self.coffee = coffee

    def get_description(self):
        pass

    def get_price(self):
        pass


class Milk(AddOn):

    def get_description(self):
        return self.coffee.get_description() + ", Milk"

    def get_price(self):
        return self.coffee.get_price() + 20


class Sugar(AddOn):

    def get_description(self):
        return self.coffee.get_description() + ", Sugar"

    def get_price(self):
        return self.coffee.get_price() + 10


class ExtraCoffee(AddOn):

    def get_description(self):
        return self.coffee.get_description() + ", Extra Coffee"

    def get_price(self):
        return self.coffee.get_price() + 30


class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, amount):
        pass

class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage):
        self.percentage = percentage

    def apply(self, amount):
        return amount * (1 - self.percentage / 100)



coffee = Espresso()

coffee = Milk(coffee)
coffee = Sugar(coffee)
coffee = ExtraCoffee(coffee)

print(coffee.get_description())
print(coffee.get_price())

discount = PercentageDiscount(20)

final_price = discount.apply(coffee.get_price())

print("final price: ", final_price)