import os
import unittest

from dotenv import load_dotenv
import requests

from src.chargily_pay.api import ChargilyClient
from src.chargily_pay.settings import CHARGILIY_TEST_URL
from src.chargily_pay.entity import (
    Customer,
    Address,
    Product,
    Price,
    Checkout,
    PaymentLink,
    PaymentItem,
)


class TestChargilyClient(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        key = os.getenv("CHARGILY_KEY")
        secret = os.getenv("CHARGILY_SECRET")
        self.chargily = ChargilyClient(key, secret, url=CHARGILIY_TEST_URL)

    def test_get_balence(self):
        response = self.chargily.get_balance()
        self.assertEqual(type(response), dict)

    def test_create_customer(self):
        customer = Customer(
            name="Username",
            email="example@gmail.com",
            address=Address(address="Address", state="State", country="dz"),
        )
        response = self.chargily.create_customer(customer)
        self.assertEqual(type(response), dict)

    def test_create_customer_with_exception(self):
        customer = Customer(
            name="Username",
            email="example@gmail.com",
            address=Address(
                address="Address", state="State", country="wrong country code"
            ),
        )
        try:
            response = self.chargily.create_customer(customer)
        except requests.exceptions.HTTPError as e:
            self.assertEqual(type(e.response.json()), dict)

    def test_create_customer_with_phone(self):
        customer = Customer(
            name="Username",
            email="example@gmail.com",
            phone="12345678",
            address=Address(address="Address", state="State", country="dz"),
        )
        response = self.chargily.create_customer(customer)
        self.assertEqual(type(response), dict)
        self.assertEqual(response["phone"], "12345678")

    def test_create_customer_without_address(self):
        customer = Customer(
            name="Username",
            email="example@gmail.com",
        )
        response = self.chargily.create_customer(customer)
        self.assertEqual(type(response), dict)

    def test_update_customer(self):
        customer = Customer(
            name="Username",
            email="example@gmail.com",
        )
        response = self.chargily.create_customer(customer)
        customer_id = response["id"]
        self.assertEqual(response["name"], "Username")
        customer.name = "Username2"
        response = self.chargily.update_customer(customer_id, customer)
        self.assertEqual(response["name"], "Username2")

    def test_get_customer(self):
        customer = Customer(name="Username", email="example@gmail.com")
        response = self.chargily.create_customer(customer)
        customer_id = response["id"]
        response = self.chargily.retrieve_customer(customer_id)
        self.assertEqual(response["name"], "Username")

    def test_delete_customer(self):
        customer = Customer(name="Username", email="example@gmail.com")
        response = self.chargily.create_customer(customer)
        customer_id = response["id"]
        response = self.chargily.delete_customer(customer_id)
        try:
            response = self.chargily.retrieve_customer(customer_id)
        except requests.exceptions.HTTPError as err:
            self.assertEqual(err.response.status_code, 404)

    # Products

    def test_create_product(self):
        product1 = Product(
            name="Product name",
        )
        response = self.chargily.create_product(product1)
        self.assertEqual(type(response), dict)

        # product4 = Product(
        #     name="Product name",
        #     description="Product description",
        #     images=["https://example.com/image.png"], # TODO: there is a bug when upload image
        #     metadata=[],
        # )

        # response = self.chargily.create_product(product4)
        # self.assertEqual(type(response), dict)

    def test_update_product(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        self.assertEqual(response["name"], "Product name")
        product.name = "Product name 2"
        response = self.chargily.update_product(product_id, product)
        self.assertEqual(response["name"], "Product name 2")

    def test_get_product(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        response = self.chargily.retrieve_product(product_id)
        self.assertEqual(response["name"], "Product name")

    def test_delete_product(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        response = self.chargily.delete_product(product_id)
        try:
            response = self.chargily.retrieve_product(product_id)
        except requests.exceptions.HTTPError as err:
            self.assertEqual(err.response.status_code, 404)

    def test_list_products(self):
        response = self.chargily.list_products()
        self.assertEqual(type(response), dict)

        response = self.chargily.list_products(per_page=1, page=1)
        self.assertEqual(type(response), dict)

    def test_retrieve_product_prices(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        response = self.chargily.retrieve_product_prices(product_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(response["data"], [])

        self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        response = self.chargily.retrieve_product_prices(product_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(response["data"]), 1)
        self.assertEqual(response["data"][0]["amount"], 100)

    # Price

    def test_create_price(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        self.assertEqual(type(price), dict)

    def test_update_price(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]

        # create price
        price = Price(amount=100, currency="dzd", product_id=product_id)
        response = self.chargily.create_price(price)

        # update price
        price_id = response["id"]
        self.assertEqual(response["amount"], 100)

        try:  # should fail, because amount is not editable
            price.amount = 200
            price = self.chargily.update_price(price_id, price)
            self.assertEqual(price["amount"], 200)
            raise Exception("Should fail")
        except requests.exceptions.HTTPError as err:
            self.assertEqual(err.response.status_code, 422)

    def test_retieve_price(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        price = self.chargily.retrieve_price(price_id)
        self.assertEqual(type(price), dict)

    def test_list_prices(self):
        response = self.chargily.list_prices()
        self.assertEqual(type(response), dict)

        response = self.chargily.list_prices(per_page=1, page=1)
        self.assertEqual(type(response), dict)

    # Create checkout
    def test_create_checkout(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
            )
        )
        self.assertEqual(type(checkout), dict)

    def test_create_checkout_with_webhook(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
                webhook_endpoint="https://example.com/webhook",
            )
        )
        self.assertEqual(type(checkout), dict)
        self.assertEqual(checkout["webhook_endpoint"], "https://example.com/webhook")

    def test_create_checkout_with_payment_method(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                payment_method="cib",
            )
        )
        self.assertEqual(type(checkout), dict)
        self.assertEqual(checkout["payment_method"], "cib")

    def test_create_checkout_with_amount(self):
        checkout = self.chargily.create_checkout(
            Checkout(
                amount=1000,
                currency="dzd",
                success_url="https://example.com/success",
            )
        )
        self.assertEqual(type(checkout), dict)

    def test_create_checkout_with_customer(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        customer = Customer(
            name="Username",
            email="customer@gmail.com",
        )
        response = self.chargily.create_customer(customer)
        customer_id = response["id"]

        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
                customer_id=customer_id,
            )
        )
        self.assertEqual(type(checkout), dict)

    def test_retieve_checkout(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
            )
        )
        checkout_id = checkout["id"]
        checkout = self.chargily.retrieve_checkout(checkout_id)
        self.assertEqual(type(checkout), dict)

    def test_list_checkouts(self):
        response = self.chargily.list_checkouts()
        self.assertEqual(type(response), dict)

        response = self.chargily.list_checkouts(per_page=1, page=1)
        self.assertEqual(type(response), dict)

    def test_retrieve_checkout_items(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
            )
        )
        checkout_id = checkout["id"]
        checkout = self.chargily.retrieve_checkout_items(checkout_id)
        self.assertEqual(type(checkout), dict)

    def test_expire_checkout(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]
        price = self.chargily.create_price(
            Price(amount=100, currency="dzd", product_id=product_id)
        )
        price_id = price["id"]
        checkout = self.chargily.create_checkout(
            Checkout(
                items=[{"price": price_id, "quantity": 1}],
                success_url="https://example.com/success",
                failure_url="https://example.com/failure",
            )
        )
        checkout_id = checkout["id"]
        checkout = self.chargily.expire_checkout(checkout_id)
        self.assertEqual(type(checkout), dict)
        self.assertEqual(checkout["status"], "expired")

    # Payment links

    def test_create_payment_link(self):
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
        )
        self.assertEqual(type(payment_link), dict)

    def test_update_payment_link(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]

        price = Price(amount=100, currency="dzd", product_id=product_id)
        response = self.chargily.create_price(price)
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
        payment_link_id = response["id"]
        self.assertEqual(response["name"], "Payment link name")
        try:
            payment_link.name = "Payment link name 2"
            response = self.chargily.update_payment_link(payment_link_id, payment_link)
            self.assertEqual(response["name"], "Payment link name 2")
            raise Exception("Should fail")
        except requests.exceptions.HTTPError as err:
            self.assertEqual(err.response.status_code, 422)

    def test_retrieve_payment_link(self):
        product = Product(
            name="Product name",
            description="Product description",
        )
        response = self.chargily.create_product(product)
        product_id = response["id"]

        price = Price(amount=100, currency="dzd", product_id=product_id)
        response = self.chargily.create_price(price)
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
        payment_link_id = response["id"]
        response = self.chargily.retrieve_payment_link(payment_link_id)
        self.assertEqual(type(response), dict)

    def test_list_payment_links(self):
        response = self.chargily.list_payment_links()
        self.assertEqual(type(response), dict)

        response = self.chargily.list_payment_links(per_page=1, page=1)
        self.assertEqual(type(response), dict)
