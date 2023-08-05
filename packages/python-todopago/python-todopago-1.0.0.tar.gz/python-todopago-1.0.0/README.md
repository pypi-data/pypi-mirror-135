# python-todopago

python-todopago is a library based on the TodoPagos's Python-SDK. The main purpose of this library is to provide a friendly and pythonic way to consume TodoPagos's services, using [zeep](https://docs.python-zeep.org/en/master/) as soap client and [requests](https://docs.python-requests.org/en/latest/) for rest client.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python-todopago.

```bash
pip install python-todopago
```

## Usage

```python
import python_todopago

# initialize connector class  
connector = TodoPagoConnector(
        "PRISMA A793D307441615AF6AAAD7497A75DE59", # token
        2159, # merchant id
        sandbox=True,
    )

# authorize operation
authorization = connector.authorize_operation(
        success_url="http://example.com/success/",
        failure_url="http://example.com/failure/",
        operation_id="ABC",
        currency=32,
        amount=2.00,
        city="Cordoba",
        country_code="AR",
        state_code="D",
        billing_first_name="Juan",
        billing_last_name="Lopez",
        billing_email="test@gmail.com",
        billing_phone="+543513840243",
        billing_postcode="5000",
        billing_address_1="Arrayan 8958",
        billing_address_2=None,
        customer_id="1",
        customer_ip_address="192.168.0.1",
        items=items, # List[Item]
    )

# get operation status
status = connector.get_operation_status(
            "1fb7cc9a-14dd-42ec-bf1e-6d5820799642", # request key
            "44caba31-1373-4544-aa6b-42abff696944", # answer key
        )

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This software is distributed under the MIT licence. See LICENCE for details.

Copyright (c) 2021-2022 Juan Pablo Senn <juanpsenn@gmail.com>
