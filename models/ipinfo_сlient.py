import requests
from models.base_сlient import BaseClient

class IPinfoClient(BaseClient):
    def __init__(self, base_url, ip):
        super().__init__(base_url)
        self.ip = ip

    def get_ip_info(self):
        response = requests.get(self.api_base_url+f"/{self.ip}/geo")
        if response.status_code == 200:
            return self._result(200,
                                "Получена информация об ip",
                                ip_info = response.json()
                                )
        error_data = self._safe_json(response)
        return self._result(response.status_code,
                            f"Ошибка получения информации по ip: {str(error_data)}")