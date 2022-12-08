from fastapi import Depends
from requests import RequestException, post

from src.infrastructure.config.app_config import ApplicationSettings, get_settings


class HateSpeechDetectionClient:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def check_review(self, json):
        try:
            return post(url=self.service_url, json=json, timeout=3).json()
        except RequestException as exception:
            print(f"Hate Speech Detection Service encountered an unexpected error: \n{exception}")


async def hate_speech_detection_client(config: ApplicationSettings = Depends(get_settings)):
    return HateSpeechDetectionClient(config.HATE_SPEECH_DETECTION_SERVICE_URL)
