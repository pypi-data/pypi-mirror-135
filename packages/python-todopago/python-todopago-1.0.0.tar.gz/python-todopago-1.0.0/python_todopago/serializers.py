from decimal import Decimal
from typing import List, Optional

from .helpers import Item, get_currency


def serialize_operation(
    merchant: int,
    operation_id: str,
    currency: int,
    amount: Decimal,
    city: str,
    country_code: str,
    state_code: str,
    billing_first_name: str,
    billing_last_name: str,
    billing_email: str,
    billing_phone: str,
    billing_postcode: str,
    billing_address_1: str,
    billing_address_2: Optional[str],
    customer_id: str,
    customer_ip_address: str,
    items: List[Item],
):
    return {
        "MERCHANT": merchant,
        "OPERATIONID": operation_id,
        "CURRENCYCODE": str(currency).zfill(3),
        "AMOUNT": "%.2f" % (amount),
        "TIMEOUT": "300000",
        "CSBTCITY": city,
        "CSSTCITY": city,
        "CSBTCOUNTRY": country_code,
        "CSSTCOUNTRY": country_code,
        "CSBTEMAIL": billing_email,
        "CSSTEMAIL": billing_email,
        "CSBTFIRSTNAME": billing_first_name,
        "CSSTFIRSTNAME": billing_first_name,
        "CSBTLASTNAME": billing_last_name,
        "CSSTLASTNAME": billing_last_name,
        "CSBTPHONENUMBER": billing_phone,
        "CSSTPHONENUMBER": billing_phone,
        "CSBTPOSTALCODE": billing_postcode,
        "CSSTPOSTALCODE": billing_postcode,
        "CSBTSTATE": state_code,
        "CSSTSTATE": state_code,
        "CSBTSTREET1": billing_address_1,
        "CSSTSTREET1": billing_address_1,
        "CSBTSTREET2": billing_address_2,
        "CSSTSTREET2": billing_address_2,
        "CSBTCUSTOMERID": str(customer_id),
        "CSBTIPADDRESS": customer_ip_address,
        "CSPTCURRENCY": get_currency(currency),
        "CSPTGRANDTOTALAMOUNT": "%.2f" % (amount),
        "CSITPRODUCTCODE": str("default#" * len(items))[:-1],
        "CSITPRODUCTDESCRIPTION": "#".join([i.description for i in items]),
        "CSITPRODUCTNAME": "#".join([i.name for i in items]),
        "CSITPRODUCTSKU": "#".join([i.sku for i in items]),
        "CSITTOTALAMOUNT": "#".join(["%.2f" % (i.amount) for i in items]),
        "CSITQUANTITY": "#".join([str(i.quantity) for i in items]),
        "CSITUNITPRICE": "#".join(["%.2f" % (i.unit_price) for i in items]),
    }


def serialize_merchant(token: str, merchant: int, success_url: str, failure_url: str):
    return {
        "Security": token[-32:],
        "Merchant": merchant,
        "URL_OK": success_url,
        "URL_ERROR": failure_url,
    }


def serialize_gaa(token: str, merchant: int, request_key: str, answer_key: str):
    return {
        "Security": token[-32:],
        "Merchant": merchant,
        "RequestKey": request_key,
        "AnswerKey": answer_key,
    }
