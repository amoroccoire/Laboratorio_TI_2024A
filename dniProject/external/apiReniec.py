from typing import List, Optional
import logging
import requests

class ApiNet:
    BASE_URL = 'https://api.apis.net.pe'

    def __init__(self, token: str = None) -> None:
        self.token = token

    def _get(self, path: str, params: dict):

        url = f"{self.BASE_URL}{path}"

        headers = {
            "Authorization": self.token, 
            "Referer": "https://apis.net.pe/api-tipo-cambio.html"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422:
            logging.warning(f"{response.url} - invalida parameter")
            logging.warning(response.text)
        elif response.status_code == 403:
            logging.warning(f"{response.url} - IP blocked")
        elif response.status_code == 429:
            logging.warning(f"{response.url} - Many requests add delay")
        elif response.status_code == 401:
            logging.warning(f"{response.url} - Invalid token or limited")
        else:
            logging.warning(f"{response.url} - Server Error status_code={response.status_code}")
        return None

    def get_person(self, dni: str) -> Optional[dict]:
        return self._get("/v2/reniec/dni", {"numero": dni})