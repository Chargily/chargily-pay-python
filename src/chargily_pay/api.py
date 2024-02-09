import hmac
import hashlib
from dataclasses import asdict

import requests
from requests.compat import urljoin

from .entity import Checkout, Customer, PaymentLink, Price, Product
from .settings import *


# drop None values
exclude_none_value = lambda x: {k: v for (k, v) in x if v is not None}

asdict_true_value = lambda x: asdict(x, dict_factory=exclude_none_value)


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
        response.raise_for_status()
        return response.json()

    # ==================================
    # Customers
    # ==================================

    def create_customer(self, customer: Customer):
        """Create a customer"""
        customer_dict = asdict_true_value(customer)
        response = requests.post(
            urljoin(self.url, "customers"), headers=self.headers, json=customer_dict
        )
        response.raise_for_status()
        return response.json()

    def update_customer(self, id, customer: Customer):
        """Update a customer"""
        customer_dict = asdict_true_value(customer)
        response = requests.post(
            urljoin(self.url, f"customers/{id}"),
            headers=self.headers,
            json=customer_dict,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_customer(self, id):
        """Retrieve a customer"""
        response = requests.get(
            urljoin(self.url, f"customers/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def list_customers(self, per_page: int = 10, page: int = 1):
        """List customers"""
        response = requests.get(
            urljoin(self.url, f"customers?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )
        response.raise_for_status()
        return response.json()

    def delete_customer(self, id):
        """Delete a customer"""
        response = requests.delete(
            urljoin(self.url, f"customers/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    # ==================================
    # Products
    # ==================================

    def create_product(self, product: Product):
        """Create a product"""
        product_dict = asdict_true_value(product)

        response = requests.post(
            urljoin(self.url, "products"),
            headers=self.headers,
            json=product_dict,
        )
        response.raise_for_status()
        return response.json()

    def update_product(self, id, product: Product):
        """Update a product"""
        product_dict = asdict_true_value(product)

        response = requests.post(
            urljoin(self.url, f"products/{id}"),
            headers=self.headers,
            json=product_dict,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_product(self, id):
        """Retrieve a product"""
        response = requests.get(
            urljoin(self.url, f"products/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def list_products(self, per_page: int = 10, page: int = 1):
        """List products"""
        response = requests.get(
            urljoin(self.url, f"products?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )
        response.raise_for_status()
        return response.json()

    def delete_product(self, id):
        """Delete a product"""
        response = requests.delete(
            urljoin(self.url, f"products/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    # todo: retrieve product prices
    def retrieve_product_prices(self, id, per_page: int = 10, page: int = 1):
        """Retrieve product prices"""
        response = requests.get(
            urljoin(self.url, f"products/{id}/prices?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )
        response.raise_for_status()
        return response.json()
     
    # ==================================
    # Prices
    # ==================================

    def create_price(self, price: Price):
        """Create a price"""
        price_dict = asdict_true_value(price)
        response = requests.post(
            urljoin(self.url, "prices"),
            headers=self.headers,
            json=price_dict,
        )
        response.raise_for_status()
        return response.json()

    def update_price(self, id, price: Price):
        """Update a price"""
        price_dict = asdict_true_value(price)
        response = requests.post(
            urljoin(self.url, f"prices/{id}"),
            headers=self.headers,
            json=price_dict,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_price(self, id):
        """Retrieve a price"""
        response = requests.get(urljoin(self.url, f"prices/{id}"), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_prices(self, per_page: int = 10, page: int = 1):
        """List prices"""
        response = requests.get(
            urljoin(self.url, f"prices?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )
        response.raise_for_status()
        return response.json()



    # ==================================
    # Checkouts
    # ==================================

    def create_checkout(self, checkout: Checkout):
        """Create a checkout"""
        checkout_dict = asdict_true_value(checkout)
        response = requests.post(
            urljoin(self.url, "checkouts"),
            headers=self.headers,
            json=checkout_dict,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_checkout(self, id):
        """Retrieve a checkout"""
        response = requests.get(
            urljoin(self.url, f"checkouts/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def list_checkouts(self, per_page: int = 10, page: int = 1):
        """List checkouts"""
        response = requests.get(
            urljoin(self.url, f"checkouts?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        response.raise_for_status()
        return response.json()

    def retrieve_checkout_items(self, id, per_page: int = 10, page: int = 1):
        """List checkouts items"""
        response = requests.get(
            urljoin(self.url, f"checkouts/{id}/items?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        response.raise_for_status()
        return response.json()

    def expire_checkout(self, id):
        """Expire a checkout"""
        response = requests.post(
            urljoin(self.url, f"checkouts/{id}/expire"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()


    # ==================================
    # Payment Links
    # ==================================
    def create_payment_link(self, payment_link: PaymentLink):
        """Create a payment link"""
        payment_link_dict = asdict_true_value(payment_link)
        response = requests.post(
            urljoin(self.url, "payment-links"),
            headers=self.headers,
            json=payment_link_dict,
        )
        response.raise_for_status()
        return response.json()

    def updata_payment_link(self, id, payment_link: PaymentLink):
        """Update a payment link"""
        payment_link_dict = asdict_true_value(payment_link)
        response = requests.post(
            urljoin(self.url, f"payment-links/{id}"),
            headers=self.headers,
            json=payment_link_dict,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_payment_link(self, id):
        """Retrieve a payment link"""
        response = requests.get(
            urljoin(self.url, f"payment-links/{id}"), headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def list_payment_links(self, per_page: int = 10, page: int = 1):
        """List payment links"""
        response = requests.get(
            urljoin(self.url, f"payment-links?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        response.raise_for_status()
        return response.json()

    def retrieve_payment_link_items(self, id, per_page: int = 10, page: int = 1):
        """List payment link items"""
        response = requests.get(
            urljoin(self.url, f"payment-links/{id}/items?page={page}"),
            headers=self.headers,
            params={"per_page": per_page},
        )

        response.raise_for_status()
        return response.json()

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


    