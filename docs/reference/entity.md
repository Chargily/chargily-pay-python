# Entity
## Address 
Represents a customer's address, including country, state, and street address.
```py
@dataclass
class Address:
    country: Optional[str] = ""
    state: Optional[str] = ""
    address: Optional[str] = ""
```

## Customer
Describes a customer with attributes like name, email, phone, address, and metadata.

```py
@dataclass
class Customer:
    name: str
    email: str
    phone: Optional[str] = None
    address: Address = None
    metadata: list = field(default_factory=list)
```

## Product
Represents a product with attributes such as name, description, images, and metadata.

```py
@dataclass
class Product:
    name: str
    description: Optional[str] = None
    images: list[str] = None
    metadata: list[dict] = field(default_factory=list)
```

## Price 
Defines the price of a product, including amount, currency, product ID, and metadata.

```py
@dataclass
class Price:
    amount: int
    currency: str
    product_id: str
    metadata: list[dict] = field(default_factory=list)
```

## Checkout
Represents a checkout session, including success and failure URLs, items, amount, currency, customer ID, and metadata.

```py
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
```

### Checkout item
Describes an item within a checkout, including a reference to a price and quantity.

```py
@dataclass
class CheckoutItem:
    price: str
    quantity: int
```

## PaymentLink 
Describe a payment session, contain name, items amd locale, after_completion_message and metadata

```py
@dataclass
class PaymentLink:
    name: str
    items: list[PaymentItem]
    after_completion_message: str = None
    locale: str = None
    pass_fees_to_customer: bool = None
    metadata: list[dict] = None
```

### PaymentLink Item
Represent an item of payment contain price which is an id of price for a product, quantity the amount of product and adjustable_quantity which enable user to edit number of items

```py
@dataclass
class PaymentItem:
    price: str
    quantity: int
    adjustable_quantity: bool = None
```