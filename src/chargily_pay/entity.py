from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Address:
    country: Optional[str] = ""
    state: Optional[str] = ""
    address: Optional[str] = ""


@dataclass
class Customer:
    name: str
    email: str
    phone: Optional[str] = None
    address: Address = None
    metadata: list = field(default_factory=list)


@dataclass
class Product:
    name: str
    description: Optional[str] = None
    images: list[str] = None
    metadata: list[dict] = field(default_factory=list)


@dataclass
class Price:
    amount: int
    currency: str
    product_id: str
    metadata: list[dict] = field(default_factory=list)


@dataclass
class CheckoutItem:
    price: str
    quantity: int


@dataclass
class Checkout:
    success_url: str
    items: Optional[CheckoutItem] = None
    amount: Optional[int] = None
    currency: str = None
    failure_url: str = None
    customer_id: str = None
    description: str = None
    locale: str = None
    payment_method: str = None
    webhook_endpoint: str = None
    pass_fees_to_customer: bool = None
    metadata: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.items and not self.amount:
            raise Exception("Either items or amount must be provided")

        if self.amount:
            if self.amount <= 10:
                raise Exception("amount should be great than 10 dzd")
            if not self.currency:
                raise Exception("Currency must be provided when amount is provided")


@dataclass
class PaymentItem:
    price: str
    quantity: int
    adjustable_quantity: bool = None


@dataclass
class PaymentLink:
    name: str
    items: list[PaymentItem]
    after_completion_message: str = None
    locale: str = None
    pass_fees_to_customer: bool = None
    metadata: list[dict] = field(default_factory=list)
