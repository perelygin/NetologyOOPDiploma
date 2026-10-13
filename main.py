import os
# import requests
# import logging
# import http.client as http_client

from pprint import pprint
from  models.ipify_сlient import IPifyClient
from  models.ipinfo_сlient import IPinfoClient
from  models.yandex_disk_client import YandexDiskClient

# # Включаем логирование HTTP-трафика
# http_client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True



searching_ip_info={}
file_name= "ipinfo.json"
folder_name="aie-9 Netology Group. Perelygin"
ip_ify_Client = IPifyClient("https://api.ipify.org")
searching_ip =ip_ify_Client.get_ip()
print(f"Статус поиска IP: {searching_ip["message"]}")
if searching_ip["status_code"] == 200:
    ip_info_Client =IPinfoClient("https://ipinfo.io",searching_ip["ip"])
    searching_ip_info = ip_info_Client.get_ip_info()
    print(f"Статуc получения информации об IP: {searching_ip_info["message"]}")
    if searching_ip_info["status_code"] == 200:
        pprint(searching_ip_info["ip_info"])
        token = os.getenv("YandexDiskToken")
        if not token:
            # raise RuntimeError("Не задан YandexDiskToken в переменных окружения")
            print("Токен для YandexDisk не доступен. Проверьте переменные окружения")
        else:
            ya_Client = YandexDiskClient("https://cloud-api.yandex.net/v1/disk", token)
            folder = ya_Client.create_folder(f"/{folder_name}")
            print(f"Статус создания каталога:{folder["message"]} " )
            if folder["status_code"] == 201 or folder["status_code"] == 409:
                load_link = ya_Client.get_upload_link(f"/{folder_name}/{file_name}")
                print(f"Статус получения ссылки для загрузки файла: {load_link["message"]}")
                if load_link["status_code"] == 200:   #ссылка для загрузки
                    loaded_file = ya_Client.download_json_data(load_link["href"], searching_ip_info["ip_info"])
                    print(f"Статус загрузки файла: {loaded_file["message"]}")
                    if loaded_file["status_code"] == 201:  #загрузка файла
                        resource_info = ya_Client.get_resource_info(f"/{folder_name}/{file_name}") #проверка загрузки файла
                        print(f"Статус получения информации о загруженном файле: {resource_info["message"]}")
                        pprint(resource_info["resource_info"])


