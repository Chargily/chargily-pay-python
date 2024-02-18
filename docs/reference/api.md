# Chargily Client
The ChargilyClient class encapsulates functionalities for interacting with the Chargily API, allowing seamless integration of payment-related operations into your Python application.

## Constructor
**Parameters:**
- `key`: Chargily API key.
- `secret`: Chargily API secret.
- `url` (optional): Chargily API base URL. Defaults to the CHARGILIY_URL specified in the settings.

## Methods
### get_balance():
**Description:** Fetches the balance associated with the Chargily account.
Returns: JSON response containing the balance information.

### create_customer(customer: Customer, *args, kwargs):
**Description:** Creates a new customer in the Chargily system.
**Parameters:**
- `customer`: An instance of the Customer data class representing customer details.

**Returns:** JSON response confirming the creation of the customer.

### update_customer(id, customer: Customer):

**Description:** Updates an existing customer's details.
**Parameters:**
- `id`: Customer ID to identify the customer.
- `customer`: An instance of the Customer data class with updated details.

**Returns:** JSON response confirming the update.

### retrieve_customer(id):
**Description:** Retrieves details of a specific customer.
**Parameters:**
- `id`: Customer ID to identify the customer.

**Returns:** JSON response containing customer details.

### list_customers(per_page: int = 10, page: int = 1):
**Description:** Lists customers with pagination support.
**Parameters:**
- `per_page (optional)`: Number of customers per page (default: 10).
- `page (optional)`: Page number for pagination (default: 1).

**Returns:** JSON response containing a list of customers.

### delete_customer(id):
**Description:** Deletes a customer based on the provided ID.
**Parameters:**
- `id`: Customer ID to identify the customer.

**Returns:** JSON response confirming the deletion.

### create_product(product: Product):
**Description:** Creates a new product in the Chargily system.
**Parameters:**
- `product`: An instance of the Product data class representing product details.

**Returns:** JSON response confirming the creation of the product.

### update_product(id, product: Product):
**Description:** Updates details of an existing product.
**Parameters:**
- `id`: Product ID to identify the product.
- `product`: An instance of the Product data class with updated details.

**Returns:** JSON response confirming the update.

### retrieve_product(id):
**Description:** Retrieves details of a specific product.
**Parameters:**
- `id`: Product ID to identify the product.

**Returns:** JSON response containing product details.

### list_products(per_page: int = 10, page: int = 1):
**Description:** Lists products with pagination support.
**Parameters:**
- `per_page` (optional): Number of products per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns:** JSON response containing a list of products.

### delete_product(id):
**Description:** Deletes a product based on the provided ID.
**Parameters:**
- `id`: Product ID to identify the product.

**Returns:** JSON response confirming the deletion.

### retrieve_product_prices(id, per_page: int = 10, page: int = 1):
**Description:** Retrieves prices associated with a specific product.
**Parameters:**
- `id`: Product ID to identify the product.
- `per_page` (optional): Number of prices per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns:** JSON response containing a list of prices.

### create_price(price: Price):
**Description:** Creates a new price in the Chargily system.
**Parameters:**
- `price`: An instance of the Price data class representing price details.

**Returns:** JSON response confirming the creation of the price.

### update_price(id, metadata: list[dict]):
**Description:** Updates metadata of an existing price.
**Parameters:**
- `id`: Price ID to identify the price.
- `metadata`: A list of dictionaries containing updated metadata.

**Returns:** JSON response confirming the update.

### retrieve_price(id):
**Description:** Retrieves details of a specific price.
**Parameters:**
- `id`: Price ID to identify the price.

**Returns**: JSON response containing price details.

### list_prices(per_page: int = 10, page: int = 1):
**Description:** Lists prices with pagination support.
**Parameters:**
- `per_page (optional)`: Number of prices per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns:** JSON response containing a list of prices.

### create_checkout(checkout: Checkout):
**Description:** Creates a new checkout in the Chargily system.
**Parameters:**
- `checkout`: An instance of the Checkout data class representing checkout details.

**Returns:** JSON response confirming the creation of the checkout.

### retrieve_checkout(id):
**Description:** Retrieves details of a specific checkout.
**Parameters:**
- `id`: Checkout ID to identify the checkout.

**Returns:** JSON response containing checkout details.

### list_checkouts(per_page: int = 10, page: int = 1):
**Description:** Lists checkouts with pagination support.
**Parameters:**
- `per_page` (optional): Number of checkouts per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns**: JSON response containing a list of checkouts.

### retrieve_checkout_items(id, per_page: int = 10, page: int = 1):
**Description**: Lists items associated with a specific checkout.
**Parameters**:
- `id`: Checkout ID to identify the checkout.
- `per_page` (optional): Number of items per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns**: JSON response containing a list of checkout items.

### expire_checkout(id):
**Description:** Expires a specific checkout, indicating the end of the payment process.
**Parameters:**
- `id`: Checkout ID to identify the checkout.

**Returns:** JSON response confirming the expiration.

### create_payment_link(payment_link: PaymentLink):
**Description:** Creates a new payment link in the Chargily system.
**Parameters:**
- `payment_link`: An instance of the PaymentLink data class representing payment link details.

**Returns:** JSON response confirming the creation of the payment link.

### update_payment_link(id, payment_link: PaymentLink):
**Description:** Updates details of an existing payment link.
**Parameters:**
- `id`: Payment link ID to identify the payment link.
- `payment_link`: An instance of the PaymentLink data class with updated details.

**Returns**: JSON response confirming the update.

### retrieve_payment_link(id):
**Description:** Retrieves details of a specific payment link.
**Parameters:**
- `id`: Payment link ID to identify the payment link.

**Returns:** JSON response containing payment link details.

### list_payment_links(per_page: int = 10, page: int = 1):
**Description:** Lists payment links with pagination support.
**Parameters:**
- `per_page` (optional): Number of payment links per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns:** JSON response containing a list of payment links.

### retrieve_payment_link_items(id, per_page: int = 10, page: int = 1):
**Description:** Lists items associated with a specific payment link.
**Parameters:**
- `id`: Payment link ID to identify the payment link.
- `per_page` (optional): Number of items per page (default: 10).
- `page` (optional): Page number for pagination (default: 1).

**Returns:** JSON response containing a list of payment link items.

### validate_signature(signature: str, payload: str):
**Description:** Validates the signature of a payload using HMAC-SHA256 with the client's secret.
**Parameters:**
- `signature`: Signature to be validated.
- `payload`: Payload to be validated.

**Returns**: True if the signature is valid; otherwise, False.