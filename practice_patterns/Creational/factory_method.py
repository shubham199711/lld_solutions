from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def payment(self, amount: int):
        pass


class StripePay(Payment):
    def payment(self, amount: int):
        print(f"payment done by strip for amount {amount}")


class CreditCard(Payment):
    def payment(self, amount: int):
        print(f"payment done by CreditCard for amount {amount}")
    


class PaymentFactory:
    @staticmethod
    def create_payment_processor(type: str) -> Payment:
        mapping = {
            "strip": StripePay,
            "CreditCard": CreditCard
        }

        if type not in mapping:
            raise KeyError("type is not vaild")
        
        return mapping[type]()


pf = PaymentFactory.create_payment_processor("strip")
pf.payment(100)

