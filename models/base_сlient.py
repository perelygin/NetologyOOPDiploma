class BaseClient:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    @staticmethod
    def _safe_json(response):
        try:
            return response.json()
        except ValueError:
            return response.text

    @staticmethod
    def _result(status_code, message, **extra):
        return {
            "status_code": status_code,
            "message": message,
            **extra
        }