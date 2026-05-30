from abc import ABC, abstractmethod

# ABC for old coffee machine
class OldCoffee(ABC):
    @abstractmethod
    def brew_coffee_old_way(self):
        raise NotImplementedError

class OldCoffeeMachine(OldCoffee):
    def brew_coffee_old_way(self):
        print("Brewing coffee old way")


# adapter for old coffee machine
class OldCoffeeMachineAdapter(ABC):
    @abstractmethod
    def brew(self):
        raise NotImplementedError

# concrete adapter for old coffee machine
class CoffeeMachineAdapter(OldCoffeeMachineAdapter):
    def __init__(self, old_coffee_machine: OldCoffee):
        self.old_coffee_machine = old_coffee_machine

    def brew(self):
        self.old_coffee_machine.brew_coffee_old_way()

if __name__ == "__main__":
    old_coffee_machine = OldCoffeeMachine()
    coffee_machine_adapter = CoffeeMachineAdapter(old_coffee_machine)
    coffee_machine_adapter.brew()