import requests
from models.base_сlient import BaseClient

class IPinfoClient(BaseClient):
    def __init__(self, base_url, ip):
        super().__init__(base_url)
        self.ip = ip

    def get_ip_info(self):
        response = requests.get(self.api_base_url+f"/{self.ip}/geo")
        if response.status_code == 200:
            return {
                "status_code": response.status_code,
                "message": "Получена информация об ip ",
                "ip_info": response.json()
            }

        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text
        return {
            "status_code": response.status_code,
            "message": f"Ошибка получения информации по ip: {str(error_data)} "
        }
