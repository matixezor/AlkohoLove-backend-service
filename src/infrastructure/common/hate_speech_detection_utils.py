import requests

from src.infrastructure.database.models.review import ReviewDatabaseHandler


async def check_review(url, json, review_db, review_id):
    try:
        response = requests.post(url, json=json, timeout=3)
    except requests.exceptions.RequestException as err:
        print(f"Hate Speech Detection Service encountered an unexpected error: \n{err}")
        return
    if response.json():
        await ReviewDatabaseHandler.machine_increase_review_report_count(review_db, review_id)
