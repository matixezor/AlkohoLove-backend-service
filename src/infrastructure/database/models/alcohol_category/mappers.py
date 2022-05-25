from src.domain.alcohol_category import AlcoholCategory
from src.domain.alcohol_category.alcohol_category_property import PropertyOut
from src.infrastructure.database.models.alcohol_category import AlcoholCategory as DbAlcoholCategory


def map_to_alcohol_category(category: DbAlcoholCategory) -> AlcoholCategory:
    return AlcoholCategory(
        id=category['_id'],
        title=category['title'],
        required=category.get('required', None),
        properties=[
            PropertyOut(
                name=_key,
                metadata=_value
            )
            for _key, _value in category['properties'].items()
        ]
    )
