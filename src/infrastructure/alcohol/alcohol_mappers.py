from pymongo.collection import Collection

from src.infrastructure.database.models.alcohol_category import AlcoholCategory
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler


def map_alcohol(
        alcohol: dict,
        collection: Collection[AlcoholCategory]
) -> dict:
    category_properties = AlcoholCategoryDatabaseHandler.get_category_by_title(
        collection, alcohol['kind']
    )['properties'].copy()
    del category_properties['kind']

    mapped_properties = [
        {
            'name': property_name,
            'display_name': property_metadata['title'],
            'value': alcohol.pop(property_name, None)
        } for property_name, property_metadata in category_properties.items()
    ]

    alcohol['additional_properties'] = mapped_properties
    return alcohol


def map_alcohols(
        alcohols: list[dict],
        collection: Collection[AlcoholCategory]
) -> list[dict]:
    return [map_alcohol(alcohol, collection) for alcohol in alcohols]
