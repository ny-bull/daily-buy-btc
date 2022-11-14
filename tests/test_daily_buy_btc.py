import os

from dotenv import load_dotenv

from daily_buy_btc import __version__

load_dotenv()

api_key = os.environ["BITBANK_API_KEY"]


def test_version():
    assert __version__ == "0.1.0"
    print(api_key)
