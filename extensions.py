import requests
import json

class APIException(Exception):
    pass

class CurrencyConverter:
    keys = {
        "доллар": "USD",
        "евро": "EUR",
        "рубль": "RUB"
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_key = CurrencyConverter.keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта '{base}' не найдена.")

        try:
            quote_key = CurrencyConverter.keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта '{quote}' не найдена.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверное количество '{amount}'")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={quote_key}")
        resp = json.loads(r.content)

        if 'Response' in resp and resp['Response'] == 'Error':
            raise APIException("Ошибка получения курса валют")

        rate = resp[quote_key]
        result = rate * amount
        return result