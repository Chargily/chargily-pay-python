# chargily-pay V2
Chargily ePay Gateway (Python Library) for Chargily API V2

![Chargily ePay Gateway](https://raw.githubusercontent.com/Chargily/epay-gateway-php/main/assets/banner-1544x500.png "Chargily ePay Gateway")

This Plugin is to integrate ePayment gateway with Chargily easily.
- Currently support payment by **CIB / EDAHABIA** cards and soon by **Visa / Mastercard** 
- This repo is recently created for **Python Library**, If you are a developer and want to collaborate to the development of this library, you are welcomed!

## installation
```bash
pip install chargily-pay
```

## Usage
```python
from chargily_pay import ChargilyClient
from chargily_pay.settings import CHARGILIY_TEST_URL
from chargily_pay.entity import Checkout

import requests

key = "YOUR_KEY"
secret = "YOUR_SECRET"

chargily = ChargilyClient(key, secret, CHARGILIY_TEST_URL)


print(chargily.get_balance())
```

