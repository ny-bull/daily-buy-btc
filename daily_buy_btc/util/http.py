import requests


def custom_get(url: str, headers: dict) -> requests.Response:
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        raise e


def custom_post(url: str, headers: dict, data: dict) -> requests.Response:
    try:
        res = requests.post(url, headers=headers, data=data)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        raise e
