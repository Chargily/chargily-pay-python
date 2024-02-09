# Chargily Pay V2

Python Library for Chargily Pay™ Gateway - V2.

The easiest and free way to integrate e-payment API through EDAHABIA of Algerie Poste and CIB of SATIM into your Python project.

## installation
```bash
pip install chargily-pay
```

## Usage
```python
from chargily_pay import ChargilyClient
from chargily_pay.settings import CHARGILIY_TEST_URL


# ==============
# Init Chargily
# ==============
key = "YOUR_KEY"
secret = "YOUR_SECRET"

chargily = ChargilyClient(key, secret, CHARGILIY_TEST_URL)

# ==============
# Get Balance
# ==============
response = chargily.get_balance()

# ==============
# Create Customer
# ==============
from chargily_pay.entity import Customer, Address

customer = Customer(
    name="Username",
    email="example@gmail.com",
    address=Address(address="Address", state="State", country="dz"),
)
response = chargily.create_customer(customer)

# ==============
# Create Product
# ==============
from chargily_pay.entity import Product

product1 = Product(
    name="Product name",
)
chargily.create_product(product1)

# ==============
# Create Price
# ==============
from chargily_pay.entity import Product, Price

product = Product(
    name="Product name",
    description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]
price = chargily.create_price(Price(amount=100, currency="dzd", product_id=product_id))

# ==============
# Create Checkout
# =============================
# Create Checkout With Product
# =============================

from chargily_pay.entity import Product, Price
from chargily_pay.entity import Checkout

product = Product(
    name="Product name",
    description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]
price = chargily.create_price(Price(amount=100, currency="dzd", product_id=product_id))
price_id = price["id"]
checkout = chargily.create_checkout(
    Checkout(
        items=[{"price": price_id, "quantity": 1}],
        success_url="https://example.com/success",
        failure_url="https://example.com/failure",
    )
)

# =============================
# Create Checkout With Product
# =============================
from chargily_pay.entity import Checkout

response = chargily.create_checkout(
    Checkout(
        amount=1000,
        currency="dzd",
        success_url="https://example.com/success",
    )
)

# =============================
# Expire Checkout
# =============================
checkout_id = "checkout_id"
chargily.expire_checkout(checkout_id)


# ==============
# Create Payment
# ==============
from chargily_pay.entity import Product, Price, PaymentItem, PaymentLink

product = Product(
    name="Product name",
    description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]

price = Price(amount=100, currency="dzd", product_id=product_id)
response = chargily.create_price(price)
price_id = response["id"]

payment_link = chargily.create_payment_link(
    PaymentLink(
        name="Payment link name",
        items=[
            PaymentItem(
                price=price_id,
                quantity=1,
            )
        ],
    )
)


```

