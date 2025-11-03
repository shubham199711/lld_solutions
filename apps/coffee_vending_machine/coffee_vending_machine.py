from abc import ABC, abstractmethod
from typing import TypedDict
from threading import Lock



class DrinkRecipe(TypedDict):
    water: int
    coffee: int

class DrinkRecipes(TypedDict):
    type: str
    charges: int
    config: DrinkRecipe

class AddonForCoffee(TypedDict, total=False):
    suger: int
    milk: bool

class CoffeType(ABC):
    def __init__(self, type: str, charges: int) -> None:
        self.type = type
        self.charges = charges

    @abstractmethod
    def make_coffee(self, addon: AddonForCoffee):
        pass

class EspressoCoffee(CoffeType):
    def __init__(self, water: int, coffee: int, type: str, charges: int) -> None:
        super().__init__(type, charges)
        self.water = water
        self.coffee = coffee
    
    def make_coffee(self, addon: AddonForCoffee):
        print(f"Made EspressoCoffee with water: {self.water} coffee: {self.coffee} and {addon['milk'] = } and {addon['suger'] = }")
        
        

class CoffeeCreator(ABC):
    @abstractmethod
    def create_coffee_recipe(self, coffee_type: str, config: DrinkRecipe, charges: int) -> CoffeType:
        raise NotImplementedError


class SimpleCoffeeCreator(CoffeeCreator):
    def create_coffee_recipe(self, coffee_type: str, config: DrinkRecipe, charges: int) -> CoffeType:
        match coffee_type:
            case 'espresso':
                return EspressoCoffee(type=coffee_type, water=config['water'], coffee=config['coffee'], charges=charges)
            case _:
                raise NotImplementedError(f"Coffee type {coffee_type} is not implemented!")


class CoffeeMachine:
    def __init__(self, drink_recipes: list[DrinkRecipes], coffee_creator: CoffeeCreator) -> None:
        self.coffee_recipes: list[CoffeType] = []
        for coffee in drink_recipes:
            self.coffee_recipes.append(coffee_creator.create_coffee_recipe(
                coffee['type'],
                config=coffee['config'],
                charges=coffee['charges']
            ))
        
        self.lock = Lock()
        self.money: int = 0
    
    def add_money(self, money_added: int):
        with self.lock:
            self.money += money_added
        
    def __return_money(self):
        print(f"Returning {self.money = }")
        self.money = 0
    
    def make_coffee(self, coffee_data: DrinkRecipes):
        with self.lock:
            for coffee in self.coffee_recipes:
                if coffee.type == coffee_data['type']:
                    if coffee.charges > self.money:
                        raise ValueError("Money is less then coffee charges")
                    coffee.make_coffee(addon=coffee_data['config'])
                    self.money -= coffee.charges
                    self.__return_money()
                    return
        
# --------------Example usges----------------

if __name__ == "__main__":
    drink_recipes = [
        {"type": "espresso", "charges": 1.5, "config": {"water": 50, "coffee": 18}}
    ]
    
    coffee_machine = CoffeeMachine(drink_recipes, SimpleCoffeeCreator())
    coffee_machine.add_money(2.0)
    result = coffee_machine.make_coffee(
        coffee_data={"type": "espresso", "charges": 1.5, "config": {"water": 50, "coffee": 18}},
        addon={"suger": 1, "milk": True}
    )
    print(result)