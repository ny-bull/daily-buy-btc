import hashlib
import hmac
import json
import os
import time
import traceback
from logging import DEBUG, getLogger

import requests
from dotenv import load_dotenv

from util.http import custom_get, custom_post

load_dotenv()

api_key = os.environ["BITBANK_API_KEY"]
api_secret = os.environ["BITBANK_API_SECRET"]

BITBANK_API_PRIVATE = "https://api.bitbank.cc"
BITBANK_API_PUBLIC = "https://public.bitbank.cc"

BTC_AMOUNT = 1500
ETH_AMOUNT = 1500

logger = getLogger(__name__)
logger.setLevel(DEBUG)


def main() -> None:
    try:
        logger.info("Buy BitCoin!!")

        # get now btc price
        price_uri = BITBANK_API_PUBLIC + "/btc_jpy/ticker"
        res: requests.Response = custom_get(price_uri, None)
        res_json = res.json()
        btc_price: str = res_json["data"]["buy"]
        logger.info(f"[BTC] Now price is {btc_price}")
        btc_amount: int = round(BTC_AMOUNT / int(btc_price), 5)

        # buy bitcoin
        req_body: dict = {"pair": "btc_jpy", "amount": str(btc_amount), "side": "buy", "type": "market"}
        req_body_str = json.dumps(req_body)

        headers = make_headers(api_key, api_secret, req_body_str)
        res = custom_post(BITBANK_API_PRIVATE + "/v1/user/spot/order", headers, req_body_str)
        logger.info(res.json())

        # get now eth price
        price_uri = BITBANK_API_PUBLIC + "/eth_jpy/ticker"
        res_json: requests.Response = requests.get(price_uri).json()
        eth_price: str = res_json["data"]["buy"]
        logger.info(f"[ETH] Now price is {eth_price}")
        eth_amount: int = round(ETH_AMOUNT / int(eth_price), 5)

        # but ethereum
        req_body: dict = {"pair": "eth_jpy", "amount": str(eth_amount), "side": "buy", "type": "market"}
        req_body_str = json.dumps(req_body)

        headers = make_headers(api_key, api_secret, req_body_str)
        res = custom_post(BITBANK_API_PRIVATE + "/v1/user/spot/order", headers, req_body_str)
        logger.info(res.json())

    except Exception:
        logger.error(traceback.format_exc())


def hmac_sign(api_secret: str, message: str) -> str:
    """
    Params:
        api_secret: str
        message: str

    Returns:
        hexdiget: str
    """
    h = hmac.new(bytearray(api_secret, "utf8"), bytearray(message, "utf8"), hashlib.sha256)
    return h.hexdigest()


def make_headers(api_key: str, api_secret: str, data: str) -> dict:
    """
    Params:
        api_key: str
        api_secret: str
        data: str

    Returns:
        headers: dict
    """
    nonce = str(int(time.time() * 1000))
    message = nonce + data
    logger.info(f"Hash message: {message}")
    return {
        "Content-Type": "application/json",
        "ACCESS-KEY": api_key,
        "ACCESS-NONCE": nonce,
        "ACCESS-SIGNATURE": hmac_sign(api_secret, message),
    }


if __name__ == "__main__":
    main()
