from decimal import Decimal

import pytest

from python_todopago.helpers import Item


@pytest.fixture
def items():
    return [
        Item("Harry Potter", "A book", "1234", Decimal(1.0), 1, Decimal(1.0)),
        Item("Harry Potter", "A book", "1234", Decimal(1.0), 1, Decimal(1.0)),
    ]


@pytest.fixture
def operation_info(items):
    return {
        "success_url": "http://example.com/success/",
        "failure_url": "http://example.com/failure/",
        "operation_id": "ABC",
        "currency": 32,
        "amount": 2.00,
        "city": "Cordoba",
        "country_code": "AR",
        "state_code": "D",
        "billing_first_name": "Juan",
        "billing_last_name": "Lopez",
        "billing_email": "test@gmail.com",
        "billing_phone": "+543513840243",
        "billing_postcode": "5000",
        "billing_address_1": "Arrayan 8958",
        "billing_address_2": None,
        "customer_id": "1",
        "customer_ip_address": "192.168.0.1",
        "items": items,
    }
