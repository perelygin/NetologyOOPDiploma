import requests
from models.base_сlient import BaseClient

class IPifyClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_ip(self):
        response = requests.get(self.api_base_url)
        if response.status_code == 200:
            return self._result(200,
                                "Получена информация об ip",
                                ip = response.text
                                )
        return self._result(response.status_code, f"Ошибка получения нашего ip: {response.text}")