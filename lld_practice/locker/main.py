from enum import Enum
from random import randint
from threading import Lock
from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timedelta

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class LockerState(Enum):
    FREE = 1
    USED = 2
    EXPERIED = 3

class Package:
    def __init__(self, package_id: str, size: Size):
        self.id = package_id
        self.size = size

class LockerSlot:
    def __init__(self, id: str,size: Size):
        self.id = id
        self.size = size
        self.package = None
        self.pickup_code = None
        self.state = LockerState.FREE
        self.used_time = None
    
    def is_available(self):
        return self.state == LockerState.FREE
    
    def allocate(self, package: Package, pickup_code: str):
        self.package = package
        self.pickup_code = pickup_code
        self.state = LockerState.USED
        self.used_time = datetime.now()
    
    def deallocate(self):
        if self.state == LockerState.EXPERIED:
            raise ValueError("Pickup window expired. Package returned to center.")
        self.package = None
        self.pickup_code = None
        self.state = LockerState.FREE
        self.used_time = None
    
    def make_experied(self):
        self.state = LockerState.EXPERIED


class LockerStratergy(ABC):
    @abstractmethod
    def find_slot(self, slots: list[LockerSlot], package_size: Size):
        pass

class LockerAllocationStrategy(LockerStratergy):
    def find_slot(self, slots: list[LockerSlot], package_size: Size) :
        for slot in slots:
            if slot.is_available() and slot.size.value >= package_size.value:
                return slot
        return None


class LockManager:
    def __init__(self, lockerStratergy: LockerStratergy):
        self.lock = Lock()
        self.locker_slots: list[LockerSlot] = []
        self.key_to_locker = {}
        self.lockFindingStretergt = lockerStratergy

    
    def add_slot(self, slot: LockerSlot):
        self.locker_slots.append(slot)

    def set_package(self, package: Package):
        with self.lock:
            slot = self.lockFindingStretergt.find_slot(self.locker_slots, package.size)
            if not slot:
                raise RuntimeError("No available locker slots for this package size.")

            pickup_code = f"AMZN-{uuid.uuid4().hex[:6].upper()}"

            slot.allocate(package, pickup_code)
            self.key_to_locker[pickup_code] = slot

            return pickup_code
    
    def retrieve_package(self, pickup_code: str) -> Package:
        with self.lock:
            if pickup_code not in self.key_to_locker:
                raise ValueError("Invalid or expired pickup code.")
                
            slot = self.key_to_locker[pickup_code]
            package = slot.package
            
            slot.deallocate()
            del self.key_to_locker[pickup_code]
            
            return package
    
    def experire_used_locker(self):
        with self.lock:
            now = datetime.now()
            for item in self.locker_slots:
                if not item.is_available() and item.state == LockerState.USED:
                    if now - item.used_time > timedelta(days=3):
                        item.make_experied()

if __name__ == "__main__":
    service = LockManager(LockerAllocationStrategy())
    
    # Initialize our system with physical slots
    service.add_slot(LockerSlot("S1", Size.SMALL))
    service.add_slot(LockerSlot("M1", Size.MEDIUM))
    
    # Simulate Driver dropping off a medium package
    my_package = Package("PKG-9921", Size.MEDIUM)
    secure_code = service.set_package(my_package)
    print(f"Package securely deposited. Customer Pickup Code: {secure_code}")
    
    # Simulate Customer picking up the package
    retrieved_pkg = service.retrieve_package(secure_code)
    print(f"Successfully retrieved package: {retrieved_pkg.id}")

    service.experire_used_locker()
        