
### Introduction:

This tutorial guides you through integrating Chargily, into your Django web application. You'll learn how to define Django models, create a service layer for API interactions, and implement a webhook view to handle payment events. 

### 1. Install Required Packages
Make sure you have Chargily pay installed. If not, you can install it using:
```py
pip install chargily-pay
```

### 2. Configure Django Settings
Ensure your Django project settings are configured properly. In your `settings.py`, set the Chargily credentials and URL:
```py
# settings.py

import environ
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")

CHARGILY_KEY = env("CHARGILY_KEY")
CHARGILY_SECRET = env("CHARGILY_SECRET")
CHARGILY_URL = "https://pay.chargily.net/test/api/v2/"
```


### 3. Define Models

In your `models.py`, you have a model named AmountCheckout. This model represents a checkout with various attributes, including the payment status, payment method, locale, and checkout URL.

```py
# models.py
class AmountCheckout(models.Model, mixins.AbstractCheckout):
    class PAYMENT_STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        CANCELED = "CANCELED", "Canceled"
        EXPIRED = "EXPIRED", "Expired"

    class PAYMENT_METHOD(models.TextChoices):
        EDAHABIA = "edahabia", "edahabia"
        CIB = "cib", "cib"

    class LOCALE(models.TextChoices):
        ENGLISH = "en", "English"
        ARABIC = "ar", "Arabic"
        FRENCH = "fr", "French"

    amount = models.IntegerField()
    entity_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD.choices, default=PAYMENT_METHOD.EDAHABIA
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(null=True, blank=True)
    locale = models.CharField(max_length=2, choices=LOCALE, default=LOCALE.FRENCH)
    status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS.choices, default=PAYMENT_STATUS.PENDING
    )
    checkout_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def on_paid(self):
        self.status = self.PAYMENT_STATUS.PAID
        self.save()

    def on_failure(self):
        self.status = self.PAYMENT_STATUS.FAILED
        self.save()

    def on_cancel(self):
        self.status = self.PAYMENT_STATUS.CANCELED
        self.save()

    def on_expire(self):
        self.status = self.PAYMENT_STATUS.EXPIRED
        self.save()

    def to_entity(self) -> Checkout:
        entity["amount"] = self.amount
        entity["currency"] = "dzd"
        entity["success_url"] = "success_url"
        entity["payment_method"] = self.payment_method
        entity["customer_id"] = customer.id
        entity["failure_url"] = None
        entity["webhook_endpoint"] = None
        entity["description"] = self.description
        entity["locale"] = self.locale
        entity["pass_fees_to_customer"] = False
        return Checkout(**entity)
```

### 4. Create Service for Checkout
In your services.py, a service function named create_checkout is defined. It uses the ChargilyClient to create a checkout and save the relevant information in the database.

```py
# services.py

from chargily_pay import ChargilyClient

from apps.chargily_pay_django import models

client: ChargilyClient = ChargilyClient(
    secret=settings.CHARGILY_SECRET,
    key=settings.CHARGILY_KEY,
    url=settings.CHARGILY_URL,
)

def create_checkout(checkout: models.Checkout) -> models.Checkout:
    try:
        response = client.create_checkout(checkout=checkout.to_entity())
        checkout.entity_id = response["id"]
        checkout.checkout_url = response["checkout_url"]
        checkout.save()
        return checkout
    except Exception as e:
        checkout.status = models.AbstractCheckout.PAYMENT_STATUS.FAILED
        checkout.save()
        raise
```

### 5. Implement Webhook Handling
In your views.py, a class-based view named WebhookView is implemented to handle Chargily webhooks. It validates the webhook signature, processes the event, and updates the checkout status accordingly.


```py
# views.py

import json

from django.views import View
from django.http import HttpResponse, JsonResponse, HttpRequest

from apps.chargily_pay_django.models import AbstractCheckout
from apps.chargily_pay_django.services import client


class WebhookView(View):
    checkout_model = Checkout

    def post(self, request: HttpRequest, *args, **kwargs):

        signature = request.headers.get("signature")
        payload = request.body.decode("utf-8")
        if not signature:
            return HttpResponse(status=400)

        if client.validate_signature(signature, payload):
            return HttpResponse(status=403)

        event = json.loads(payload)

        checkout_id = event["data"]["id"]
        checkout = self.checkout_model.objects.get(entity_id=checkout_id)

        checkout_status = event["type"]
        if checkout_status == "checkout.paid":
            checkout.on_paid()
        elif checkout_status == "checkout.failed":
            checkout.on_failure()
        elif checkout_status == "checkout.canceled":
            checkout.on_cancel()
        elif checkout_status == "checkout.expired":
            checkout.on_expire()
        else:
            return HttpResponse(status=400)

        return JsonResponse({}, status=200)


```

### 6. Configure URLs
In your urls.py, a URL pattern is set up to route webhook requests to the WebhookView:

```py
# urls.py

from django.urls import path
from apps.chargily_pay_django.views import WebhookView

urlpatterns = [
    path("webhook/", WebhookView.as_view(), name="webhook"),
]
```