from dotenv import load_dotenv
import os

def test_version():
    load_dotenv()
    api_key = os.environ("API_KEY")
    print(api_key)
