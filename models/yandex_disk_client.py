import pprint
import json
import requests
from models.base_сlient import BaseClient

class YandexDiskClient(BaseClient):
    def __init__(self,base_url,token):
        super().__init__(base_url)
        self.token = token

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def create_folder(self, folder_name):
        params = {"path": folder_name}
        headers = self._headers()
        response = requests.put(self.api_base_url+"/resources", params=params, headers=headers)
        if response.status_code == 201:  #Folder created
            return self._result(201,
                                f"каталог {folder_name} создан")
        if response.status_code == 409:  # Folder created
            return self._result(409,
                                f"каталог {folder_name} уже существует")
        error_data = self._safe_json(response)
        return self._result(response.status_code, str(error_data))

    def get_upload_link(self, full_file_name):
        params = {"path": full_file_name}
        headers = self._headers()
        response = requests.get(self.api_base_url + "/resources/upload",
                                params=params,
                                headers=headers)
        if response.status_code == 200:
            return self._result(200,
                                f"Получена ссылка для загрузки файла {full_file_name}",
                                href = response.json()["href"])
        error_data = self._safe_json(response)
        return self._result(response.status_code,
                            f"Ошибка получения ссылки для загрузки файла. Код: {str(error_data)} ")

    def get_resource_info(self, resource_name):
        params = {"path": resource_name}
        headers = self._headers()
        response = requests.get(self.api_base_url + "/resources", params=params, headers=headers)
        if response.status_code == 200:
            return self._result(200,
                                f"Получена информация о ресурсе",
                                resource_info = response.json())
        error_data = self._safe_json(response)
        return self._result(response.status_code,
                            f"Ошибка получения информации о ресурсе. Код: {str(error_data)} ")

    def download_json_data(self, href, json_data):
        body = json.dumps(json_data, ensure_ascii=False).encode("utf-8")
        response = requests.put(href, data=body)
        if response.status_code == 201:
            return self._result(201, f"Файл  загружен.")
        return self._result(response.status_code,
                            f"Ошибка загрузки файла. Код: {str(response.text)} ")

