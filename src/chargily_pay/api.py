import hmac
import hashlib
from dataclasses import asdict

import requests
from requests.compat import urljoin

from .entity import Checkout, Customer, PaymentLink, Price, Product
from .settings import CHARGILIY_URL


# drop None values
exclude_none_value = lambda x: {k: v for (k, v) in x if v is not None}

asdict_true_value = lambda x: asdict(x, dict_factory=exclude_none_value)


def response_or_exception(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        response: requests.Response = fn(*args, **kwargs)
        if response.status_code == 422:
            raise requests.exceptions.HTTPError(response, response=response)
        response.raise_for_status()

        return response.json()

    return wrapper


class ChargilyClient:
    def __init__(self, key, secret, url=CHARGILIY_URL):
        self.key = key
        self.url = url
        self.secret = secret
        self.headers = {
            "Authorization": f"Bearer {self.secret}",
            "Content-Type": "application/json",
        }

    # ==================================
    # Balance
    # ==================================

    def get_balance(self):
        """Get your balance"""
        response = requests.get(urljoin(self.url, "balance"), headers=self.headers)

        return response.json()

    # ==================================
    # Customers
    # ==================================
    @response_or_exception
    def create_customer(self, customer: Customer, *args, **kwargs):
        """Create a customer"""
        customer_dict = asdict_true_value(customer)
        response = requests.post(
            urljoin(self.url, "customers"), headers=self.headers, json=customer_dict
        )
        return response

    @response_or_exception
    def update_customer(self, id, customer: Customer):
        """Update a customer"""
        customer_dict = asdict_true_value(customer)
        response = requests.post(
            urljoin(self.url, f"customers/{id}"),
            headers=self.headers,
            json=customer_dict,
        )

        return response

    @response_or_exception
    def retrieve_customer(self, id):
        """Retrieve a customer"""
        response = requests.get(
            urljoin(self.url, f"customers/{id}"), headers=self.headers
        )
        return response

    @response_or_exception
    def list_customers(self, per_page: int = 10, page: int = 1):
        """List customers"""
        response = requests.get(
            urljoin(self.url, f"customers?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    @response_or_exception
    def delete_customer(self, id):
        """Delete a customer"""
        response = requests.delete(
            urljoin(self.url, f"customers/{id}"), headers=self.headers
        )

        return response

    # ==================================
    # Products
    # ==================================
    @response_or_exception
    def create_product(self, product: Product):
        """Create a product"""
        product_dict = asdict_true_value(product)

        response = requests.post(
            urljoin(self.url, "products"),
            headers=self.headers,
            json=product_dict,
        )

        return response

    @response_or_exception
    def update_product(self, id, product: Product):
        """Update a product"""
        product_dict = asdict_true_value(product)

        response = requests.post(
            urljoin(self.url, f"products/{id}"),
            headers=self.headers,
            json=product_dict,
        )

        return response

    @response_or_exception
    def retrieve_product(self, id):
        """Retrieve a product"""
        response = requests.get(
            urljoin(self.url, f"products/{id}"), headers=self.headers
        )

        return response

    @response_or_exception
    def list_products(self, per_page: int = 10, page: int = 1):
        """List products"""
        response = requests.get(
            urljoin(self.url, f"products?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    def delete_product(self, id):
        """Delete a product"""
        response = requests.delete(
            urljoin(self.url, f"products/{id}"), headers=self.headers
        )

        return response

    # todo: retrieve product prices
    @response_or_exception
    def retrieve_product_prices(self, id, per_page: int = 10, page: int = 1):
        """Retrieve product prices"""
        response = requests.get(
            urljoin(self.url, f"products/{id}/prices?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    # ==================================
    # Prices
    # ==================================

    @response_or_exception
    def create_price(self, price: Price):
        """Create a price"""
        price_dict = asdict_true_value(price)
        response = requests.post(
            urljoin(self.url, "prices"),
            headers=self.headers,
            json=price_dict,
        )

        return response

    @response_or_exception
    def update_price(self, id, price: Price):
        """Update a price"""
        price_dict = asdict_true_value(price)
        response = requests.post(
            urljoin(self.url, f"prices/{id}"),
            headers=self.headers,
            json=price_dict,
        )

        return response

    @response_or_exception
    def retrieve_price(self, id):
        """Retrieve a price"""
        response = requests.get(urljoin(self.url, f"prices/{id}"), headers=self.headers)

        return response

    @response_or_exception
    def list_prices(self, per_page: int = 10, page: int = 1):
        """List prices"""
        response = requests.get(
            urljoin(self.url, f"prices?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    # ==================================
    # Checkouts
    # ==================================

    @response_or_exception
    def create_checkout(self, checkout: Checkout):
        """Create a checkout"""
        checkout_dict = asdict_true_value(checkout)
        response = requests.post(
            urljoin(self.url, "checkouts"),
            headers=self.headers,
            json=checkout_dict,
        )

        return response

    @response_or_exception
    def retrieve_checkout(self, id):
        """Retrieve a checkout"""
        response = requests.get(
            urljoin(self.url, f"checkouts/{id}"), headers=self.headers
        )

        return response

    @response_or_exception
    def list_checkouts(self, per_page: int = 10, page: int = 1):
        """List checkouts"""
        response = requests.get(
            urljoin(self.url, f"checkouts?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    @response_or_exception
    def retrieve_checkout_items(self, id, per_page: int = 10, page: int = 1):
        """List checkouts items"""
        response = requests.get(
            urljoin(self.url, f"checkouts/{id}/items?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    @response_or_exception
    def expire_checkout(self, id):
        """Expire a checkout"""
        response = requests.post(
            urljoin(self.url, f"checkouts/{id}/expire"), headers=self.headers
        )

        return response

    # ==================================
    # Payment Links
    # ==================================
    @response_or_exception
    def create_payment_link(self, payment_link: PaymentLink):
        """Create a payment link"""
        payment_link_dict = asdict_true_value(payment_link)
        response = requests.post(
            urljoin(self.url, "payment-links"),
            headers=self.headers,
            json=payment_link_dict,
        )

        return response

    @response_or_exception
    def update_payment_link(self, id, payment_link: PaymentLink):
        """Update a payment link"""
        payment_link_dict = asdict_true_value(payment_link)
        response = requests.post(
            urljoin(self.url, f"payment-links/{id}"),
            headers=self.headers,
            json=payment_link_dict,
        )

        return response

    @response_or_exception
    def retrieve_payment_link(self, id):
        """Retrieve a payment link"""
        response = requests.get(
            urljoin(self.url, f"payment-links/{id}"), headers=self.headers
        )

        return response

    @response_or_exception
    def list_payment_links(self, per_page: int = 10, page: int = 1):
        """List payment links"""
        response = requests.get(
            urljoin(self.url, f"payment-links?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    @response_or_exception
    def retrieve_payment_link_items(self, id, per_page: int = 10, page: int = 1):
        """List payment link items"""
        response = requests.get(
            urljoin(self.url, f"payment-links/{id}/items?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        return response

    # ==================================
    # Utils
    # ==================================

    def validate_signature(self, signature: str, payload: str):
        computed_signature = hmac.new(
            self.secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if hmac.compare_digest(signature, computed_signature):
            return True
        return False
