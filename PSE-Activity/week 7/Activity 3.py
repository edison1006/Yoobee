from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Credit Card"


class PayPalPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via PayPal"


class BankTransferPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Bank Transfer"


class CryptoPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Crypto"


class GooglePayPayment(PaymentMethod):
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount:.2f} via Google Pay"

class PaymentFactory:
    @staticmethod
    def create_payment(method: str) -> PaymentMethod:
        method = method.lower()
        if method == "creditcard" or method == "credit_card":
            return CreditCardPayment()
        elif method == "paypal":
            return PayPalPayment()
        elif method == "bank_transfer":
            return BankTransferPayment()
        elif method == "crypto":
            return CryptoPayment()
        elif method == "googlepay" or method == "google_pay":
            return GooglePayPayment()
        else:
            raise ValueError(f"Unknown payment method: {method}")

class PaymentGateway:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PaymentGateway, cls).__new__(cls)
        return cls._instance

    def process(self, method: str, amount: float) -> str:
        payment_obj = PaymentFactory.create_payment(method)
        return payment_obj.process_payment(amount)

if __name__ == "__main__":
    gateway1 = PaymentGateway()
    gateway2 = PaymentGateway()

    print(gateway1 is gateway2)  

    methods = ["creditcard", "paypal", "bank_transfer", "crypto", "googlepay"]
    for m in methods:
        print(gateway1.process(m, 199.99))
