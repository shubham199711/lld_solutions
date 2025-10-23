from abc import ABC, abstractmethod
from threading import Lock

class Item:
    def __init__(self, name: str, price: float, inventory: int) -> None:
        self.name = name
        self.price = price
        self.inventory = inventory
        self.lock = Lock()

    def take_item(self, count: int):
        if count > self.inventory:
            raise ValueError("Not enough items available")
        with self.lock:
            self.inventory -= count

class Coin:
    def __init__(self, amount: float, count: int) -> None:
        self.amount = amount
        self.count = count
        self.lock = Lock()

    def add(self, n: int):
        with self.lock:
            self.count += n

    def remove(self, n: int):
        with self.lock:
            if n > self.count:
                raise ValueError("Insufficient coins")
            self.count -= n

class CalculateChangeStrategy(ABC):
    @abstractmethod
    def calculate_change(self, coins: list[Coin], change_amount: float) -> list[Coin]:
        pass

class IndianCalculateChangeStrategy(CalculateChangeStrategy):
    def calculate_change(self, coins: list[Coin], change_amount: float) -> list[Coin]:
        change = []
        change_amount = round(change_amount, 2)
        for coin in sorted(coins, key=lambda c: c.amount, reverse=True):
            use = int(min(change_amount // coin.amount, coin.count))
            if use > 0:
                change.append(Coin(coin.amount, use))
                change_amount = round(change_amount - (use * coin.amount), 2)
        if change_amount > 0:
            raise ValueError("Not enough change available")
        return change

class VendingMachine:
    def __init__(self, items: dict[str, dict], coins: dict[float, int]):
        self.items = {name: Item(name, v["price"], v["inventory"]) for name, v in items.items()}
        self.coins = [Coin(amt, cnt) for amt, cnt in coins.items()]
        self.inserted = []
        self.lock = Lock()
        self.change_strategy = IndianCalculateChangeStrategy()

    def insert_coin(self, amount: float):
        self.inserted.append(amount)

    def select_product(self, name: str) -> str:
        with self.lock:
            if name not in self.items:
                raise ValueError("Invalid product")
            item = self.items[name]
            total = sum(self.inserted)
            if total < item.price:
                raise ValueError("Insufficient funds")
            item.take_item(1)
            change = self.change_strategy.calculate_change(self.coins, total - item.price)
            self.inserted.clear()
            return f"Dispensed {name}, Change: {[ (c.amount, c.count) for c in change ]}"




if __name__ == "__main__":
    vm = VendingMachine(
    {"Coke": {"price": 1.25, "inventory": 5}, "Chips": {"price": 0.75, "inventory": 3}},
        {1.0: 10, 0.25: 20}
    )
    vm.insert_coin(1.0)
    vm.insert_coin(0.5)
    print(vm.select_product("Coke"))