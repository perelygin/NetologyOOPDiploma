import pprint
import json
import requests
from models.base_сlient import BaseClient

class YandexDiskClient(BaseClient):
    def __init__(self,base_url,token):
        super().__init__(base_url)
        self.token = token

    def create_folder(self, folder_name):
        params = {"path": folder_name}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
        response = requests.put(self.api_base_url+"/resources", params=params, headers=headers)
        if response.status_code == 201:  #Folder created
            return {
                    "status_code": response.status_code,
                    "message": f"каталог {folder_name} создан"
                    }
        if response.status_code == 409:  # Folder created
            return {
                    "status_code": response.status_code,
                    "message": f"каталог {folder_name} уже существует"
                    }

        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        return {
                "status_code": response.status_code,
                "message": str(error_data)
                }


    def get_upload_link(self, full_file_name):
        params = {"path": full_file_name}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
        response = requests.get(self.api_base_url + "/resources/upload", params=params, headers=headers)
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        if response.status_code == 200:
            return {
                    "status_code": response.status_code,
                    "message": f"Получена ссылка для загрузки файла {full_file_name}",
                    "href": response.json()["href"]
                    }

        return {
                "status_code": response.status_code,
                "message": f"Ошибка получения ссылки для загрузки файла. Код: {str(error_data)} "
            }

    def get_resource_info(self, resource_name):
        params = {"path": resource_name}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
        response = requests.get(self.api_base_url + "/resources", params=params, headers=headers)
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        if response.status_code == 200:
            return {
                    "status_code": response.status_code,
                    "message": f"Получена информация о ресурсе",
                    "resource_info": response.json()
                    }

        return {
                "status_code": response.status_code,
                "message": f"Ошибка получения информации о ресурсе. Код: {str(error_data)} "
            }

    def download_json_data(self, href, json_data):
        body = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
        response = requests.put(href, data=body)
        if response.status_code == 201:
            return {
                "status_code": response.status_code,
                "message": f"Файл  загружен."
            }

        return {
            "status_code": response.status_code,
            "message": f"Ошибка загрузки файла. Код: {str(response.text)} "
        }

