from dataclasses import dataclass

import requests

from schema import GoogleUserData
from settings import Setting


@dataclass
class GoogleClient:
    settings: Setting


    def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorization": f"Bearer {access_token}"})
        return GoogleUserData(**user_info.json(), access_token=access_token)

    def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code"
        }
        response = requests.post(url=self.settings.GOOGLE_TOKEN_URI, data=data)
        print(response.json())
        return response.json()["access_token"]