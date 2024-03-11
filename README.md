# Welcome to Python Package Repository
# for [Chargily Pay](https://chargily.com/business/pay "Chargily Pay")™ Gateway - V2.

Thank you for your interest in Python Package of Chargily Pay™, an open source project by Chargily, a leading fintech company in Algeria specializing in payment solutions and  e-commerce facilitating, this Package is providing the easiest and free way to integrate e-payment API through widespread payment methods in Algeria such as EDAHABIA (Algerie Post) and CIB (SATIM) into your Python/Django projects.

This package is developed by **Tarek Berkane ([tarek-berkane](https://github.com/tarek-berkane))** and is open to contributions from developers like you.

## Installation
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

## Documentation For frameworks

-   [Django](https://github.com/Chargily/chargily-pay-python/blob/main/docs/examples/django.md)


## About Chargily Pay™ packages

Chargily Pay™ packages/plugins are a collection of open source projects published by Chargily to facilitate the integration of our payment gateway into different programming languages and frameworks. Our goal is to empower developers and businesses by providing easy-to-use tools to seamlessly accept payments.

## API Documentation

For detailed instructions on how to integrate with our API and utilize Chargily Pay™ in your projects, please refer to our [API Documentation](https://dev.chargily.com/pay-v2/introduction). 

## Developers Community

Join our developer community on Telegram to connect with fellow developers, ask questions, and stay updated on the latest news and developments related to Chargily Pay™ : [Telegram Community](https://chargi.link/PayTelegramCommunity)

## How to Contribute

We welcome contributions of all kinds, whether it's bug fixes, feature enhancements, documentation improvements, or new plugin/package developments. Here's how you can get started:

1. **Fork the Repository:** Click the "Fork" button in the top-right corner of this page to create your own copy of the repository.

2. **Clone the Repository:** Clone your forked repository to your local machine using the following command:

```bash
git clone https://github.com/Chargily/chargily-pay-python.git
```

3. **Make Changes:** Make your desired changes or additions to the codebase. Be sure to follow our coding standards and guidelines.

4. **Test Your Changes:** Test your changes thoroughly to ensure they work as expected.

5. **Submit a Pull Request:** Once you're satisfied with your changes, submit a pull request back to the main repository. Our team will review your contributions and provide feedback if needed.

## Get in Touch

Have questions or need assistance? Join our developer community on [Telegram](https://chargi.link/PayTelegramCommunity) and connect with fellow developers and our team.

We appreciate your interest in contributing to Chargily Pay™! Together, we can build something amazing.

Happy coding!
