from requests import RequestException, get
from fastapi import HTTPException, status, Depends

from src.infrastructure.config.app_config import ApplicationSettings, get_settings


class RecommenderClient:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def fetch_recommendations(self, user_id: str):
        try:
            return get(url=f'{self.service_url}/recommend/users/{user_id}').json()
        except RequestException as exception:
            raise RecommenderClientFetchRecommendationsException(user_id, str(exception))

    def fetch_similar_alcohols(self, alcohol_id: str):
        try:
            return get(url=f'{self.service_url}/recommend/alcohols/{alcohol_id}').json()
        except RequestException as exception:
            raise RecommenderClientSimilarAlcoholsException(alcohol_id, str(exception))


class RecommenderClientFetchRecommendationsException(HTTPException):
    def __init__(self, user_id: str, details: str):
        super().__init__(
            status.HTTP_502_BAD_GATEWAY,
            f'There was an error fetching recommendations for user [{user_id}] details [{details}]'
        )


class RecommenderClientSimilarAlcoholsException(HTTPException):
    def __init__(self, user_id: str, details: str):
        super().__init__(
            status.HTTP_502_BAD_GATEWAY,
            f'There was an error fetching similar alcohols for alcohol [{user_id}] details [{details}]'
        )


async def recommender_client(config: ApplicationSettings = Depends(get_settings)):
    return RecommenderClient(config.RECOMMENDER_URL)
