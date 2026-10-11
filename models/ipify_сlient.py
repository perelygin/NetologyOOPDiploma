import requests
from models.base_сlient import BaseClient

class IPifyClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url)

    def get_ip(self):
        response = requests.get(self.api_base_url)
        if response.status_code == 200:
            return {
                "status_code": response.status_code,
                "message": f"Получен наш ip: {response.text}",
                "ip": response.text
            }
        return {
                "status_code": response.status_code,
                "message": f"Ошибка получения нашего ip: {response.text}"
        }