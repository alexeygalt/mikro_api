from dataclasses import dataclass
import requests
from requests.exceptions import HTTPError, RequestException
from exeptions import GoogleAuthError
from schema.auth import GoogleUserData, YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData:
        try:
            access_token = self._get_access_token(code)

            user_info = requests.get(f"https://login.yandex.ru/info?format=json&access_token",
                                     headers={"Authorization": f"OAuth {access_token}"})
            user_info.raise_for_status()

            return YandexUserData(**user_info.json(), access_token=access_token)

        except RequestException as req_err:
            raise GoogleAuthError(f"Network error occurred: {req_err}")

        except ValueError as json_err:
            raise GoogleAuthError(f"Error parsing user info JSON: {json_err}")

    def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_SECRET_KEY,
            "grant_type": "authorization_code"
        }
        try:
            response = requests.post(self.settings.YANDEX_TOKEN_URL, data=data,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
            response.raise_for_status()
        except HTTPError as http_err:
            raise GoogleAuthError(f"HTTP error occurred during token request: {http_err}")

        except RequestException as req_err:
            raise GoogleAuthError(f"Network error occurred during token request: {req_err}")

        except KeyError:
            raise GoogleAuthError("Access token not found in response.")

        except ValueError as json_err:
            raise GoogleAuthError(f"Error parsing token JSON: {json_err}")
        return response.json()['access_token']
