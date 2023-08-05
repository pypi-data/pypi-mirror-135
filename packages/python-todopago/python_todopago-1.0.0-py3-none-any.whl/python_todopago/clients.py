from zeep import Client, Settings

wsdl = "python_todopago/wsdl/Authorize.wsdl"
ENDPOINTS = {
    True: "https://developers.todopago.com.ar/services/t/1.1/",
    False: "https://apis.todopago.com.ar/services/t/1.1/",
}


def get_client(token: str, sandbox: bool = False) -> Client:
    endpoiont = ENDPOINTS[sandbox]
    settings = Settings(extra_http_headers={"Authorization": token})
    client = Client(endpoiont + "Authorize?wsdl", settings=settings)
    client.service._binding_options["address"] = endpoiont + "Authorize"
    return client
