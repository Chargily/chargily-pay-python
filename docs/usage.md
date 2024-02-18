# Initialization
the first step you need to do is to import Chargiliy client and initialize it 
```py
from src.chargily_pay.api import ChargilyClient
from src.chargily_pay.settings import CHARGILIY_TEST_URL # or CHARGILIY_URL for production

key="chargilly-key"
secret="chargily-secret"
chargily = ChargilyClient(key, secret, url=CHARGILIY_TEST_URL)
```

## Retrieve balance
Retrieves the current account (based the API Secret Key employed in the request) balance for the three wallets (DZD, EUR, and USD).
```py
response = chargily.get_balance()
```

## Customers
R epresents a	 customer of your business.
### Create a customer
Creates a new customer.
```py
from src.chargily_pay.entity import Customer, Address

customer = Customer(
	name="Username",
	email="example@gmail.com",
	address=Address(address="Address", state="State", country="dz"),
)
response = chargily.create_customer(customer)
```

### Update a customer
Updates the information of a customer by defining the values for the passed parameters. Any parameters not supplied will remain unaltered.

```py
from src.chargily_pay.entity import Customer, Address

customer = Customer(
	name="Username",
	email="example@gmail.com",
)
response = chargily.create_customer(customer)
customer_id = response["id"]
customer.name = "Username2"
response = chargily.update_customer(customer_id, customer)
```

### Retrieve a customer
Retrieves all the information of an already-existing customer by providing it’s unique identifier (ID).

```py
from src.chargily_pay.entity import Customer

customer = Customer(name="Username", email="example@gmail.com")
response = chargily.create_customer(customer)
customer_id = response["id"]
response = chargily.retrieve_customer(customer_id)
```

### List all customers
Returns a list of all your customers.
```py
response = chargily.list_customers()
```

### Delete a customer
Deletes an already-existing customer.
```py
from src.chargily_pay.entity import Customer

customer = Customer(name="Username", email="example@gmail.com")
response = chargily.create_customer(customer)
customer_id = response["id"]
response = chargily.delete_customer(customer_id)
```


## Product
Products represent the goods or services you are selling to your customers.

### Create a product
Creates a new product.
```py
from src.chargily_pay.entity import Product

product1 = Product(
	name="Product name",
)
response = chargily.create_product(product1)
```

### Update a Product
Updates the information of a product by defining the values for the passed parameters. Any parameters not supplied will remain unaltered.

```py
from src.chargily_pay.entity import Product

product = Product(
	name="Product name",
	description="Product description",
)
response =  chargily.create_product(product)
product_id = response["id"]
product.name = "Product name 2"
response = chargily.update_product(product_id, product)
```

### Retrieve a product
Retrieves all the information of an already-existing product by providing it’s unique identifier (ID).

```py
from src.chargily_pay.entity import Product

product = Product(
	name="Product name",
	description="Product description",
)
response =  chargily.create_product(product)
product_id = response["id"]
response = chargily.retrieve_product(product_id)
```

### List all products
Returns a list of all your customers.

```py
response = chargily.list_products()
```

### Retrieve a products's prices
Retrieves all the prices of a product.

```py
response = chargily.retrieve_product_prices(product_id)
```

## The Price object
Prices define the unit cost and the currency of products. A product can have multiple prices.

### Create a price
Creates a new price.

```py
from src.chargily_pay.entity import Product, Price

product = Product(
	name="Product name",
	description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]
price = chargily.create_price(
	Price(amount=100, currency="dzd", product_id=product_id)
)

```

### Update a price
Updates the information of a price by defining the values for the passed parameters. Any parameters not supplied will remain unaltered.

```py
from src.chargily_pay.entity import Product, Price

product = Product(
	name="Product name",
	description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]

# create price
price = Price(amount=100, currency="dzd", product_id=product_id)
response = chargily.create_price(price)

# update price
# update only metadata is allowed
price_id = response["id"]
price = chargily.update_price(price_id, [{"value": "value"}])
```

### Retrieve a price
Retrieves all the information of an already-existing price by providing it’s unique identifier (ID).

```py
price = chargily.retrieve_price(price_id)
```


### List all prices
Returns a list of all your prices.

```py
response = chargily.list_prices()
response = chargily.list_prices(per_page=1, page=1)
```

## Checkout 
A Checkout is used to make your customers make a payment. Each time your customer wants to pay, you have to create a new Checkout.

### Create a checkout
#### Create a checkout with price items

```py
from src.chargily_pay.entity import Product, Price, Checkout, CheckoutItem

# create product
product = Product(
	name="Product name",
	description="Product description",
)
response = chargily.create_product(product)

#  create price
product_id = response["id"]
price = chargily.create_price(
	Price(amount=400, currency="dzd", product_id=product_id)
)

# create checkout
price_id = price["id"]
checkout = chargily.create_checkout(
	Checkout(
		items=[CheckoutItem(price=price_id, quantity=2)],
		success_url="https://example.com/success",
		failure_url="https://example.com/failure",
		payment_method="cib",
	)
)
```


#### Create a checkout with amount

```
chargily.create_checkout(
	Checkout(
		amount=1000,
		currency="dzd",
		success_url="https://example.com/success",
	)
)
```

### Retrieve a checkout

```py
checkout = chargily.retrieve_checkout(checkout_id)
```

###  List checkouut

```py
response = chargily.list_checkouts()
```

### Retrieve a checkout's items

```py
checkout = chargily.retrieve_checkout_items(checkout_id)
```

### Expire a checkout

```py
checkout = chargily.expire_checkout(checkout_id)
```

## The Payment Link object
A Payment Link is a URL that can be shared and when accessed, directs your customers to a hosted payment page. This link can be utilized multiple times. Every time a customer accesses the link, a new Checkout is generated.

### Create a payment link

```py
from src.chargily_pay.entity import Product, Price, PaymentLink, PaymentItem

product = Product(
	name="Product name",
	description="Product description",
)
response = self.chargily.create_product(product)
product_id = response["id"]

price = Price(amount=100, currency="dzd", product_id=product_id)
response = self.chargily.create_price(price)
price_id = response["id"]

payment_link = self.chargily.create_payment_link(
	PaymentLink(
		name="Payment link name",
		items=[
			PaymentItem(
				price=price_id,
				quantity=1,
			)
		],
	)
```

### Update a Payment Link
```py

product = Product(
	name="Product name",
	description="Product description",
)
response = chargily.create_product(product)
product_id = response["id"]

price = Price(amount=100, currency="dzd", product_id=product_id)
response = self.chargily.create_price(price)

# create payment
price_id = response["id"]
payment_link = PaymentLink(
	name="Payment link name",
	items=[
		PaymentItem(
			price=price_id,
			quantity=1,
		)
	],
)
response = self.chargily.create_payment_link(payment_link)

# update payment
payment_link_id = response["id"]
payment_link.name = "Payment link name 2"
response = self.chargily.update_payment_link(payment_link_id, payment_link)
```

### Retrieve a payment link
Retrieves all the information of an already-existing payment link by providing it’s unique identifier (ID).

```py
response = chargily.retrieve_payment_link(payment_link_id)
```

### List all payment links
Returns a list of all your payment links.

```py
response = chargily.list_payment_links()
```

### Retrieve a payment link's items
Retrieves all the items of a payment link.

```py
response = chargily.retrieve_payment_link_items(payment_link_id)
```