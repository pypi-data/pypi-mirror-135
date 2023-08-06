# Smartpay Python SDK

The Smartpay Python SDK offers easy access to Smartpay API from applications written in Python.

## Prerequisites

Python v3+

## Installation

```shell
pip install --save smartpay
```

## Usage

The package needs to be configured with your own API keys, you can find them on your [dashboard](https://dashboard.smartpay.co/settings/credentials).

```python
from smartpay import Smartpay

smartpay = Smartpay('<YOUR_SECRET_KEY>', public_key='<YOUR_PUBLIC_KEY>');
```

If you would like to know how Smartpay payment works, please see the [payment flow](https://docs.smartpay.co/#payment_flow) for more details.

### Create Checkout session

```python
payload = {
  items: [
    {
      name: "レブロン 18 LOW",
      amount: 250,
      currency: "JPY",
      quantity: 1,
    },
  ],

  shipping: {
    line1: "line1",
    locality: "locality",
    postalCode: "123",
    country: "JP",
  },

  # Your internal reference of the order
  reference: "order_ref_1234567",

  # Callback URLs
  successUrl: "https://docs.smartpay.co/example-pages/checkout-successful",
  cancelUrl: "https://docs.smartpay.co/example-pages/checkout-canceled",

  test: true,
};

session = smartpay.create_checkout_session(payload);
```

### To retreive the session URL

```javascript
sessionURL = smartpay.get_session_url(session);
```

We also prepare a more [real-world example](https://github.com/smartpay-co/integration-examples/blob/main/server/python/server.py) for you to refer to.
