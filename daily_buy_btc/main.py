import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ('BITBANK_API_KEY')
api_secret =  os.environ('BITBANK_API_SECRET')

def main():
    print(api_key)


if __name__ == "__main__":
    main()   