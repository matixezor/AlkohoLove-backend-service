from pymongo.collection import Collection

from src.infrastructure.database.models.alcohol_filter import AlcoholFilter


class AlcoholFilterDatabaseHandler:
    @staticmethod
    async def update_filters(
            collection: Collection[AlcoholFilter],
            kind: str,
            alcohol_type: str,
            country: str,
            color: str
    ) -> None:
        collection.update_one(
            {'_id': kind},
            {
                '$addToSet': {
                    'type': alcohol_type,
                    'country': country,
                    'color': color}
            }
        )

    @staticmethod
    async def get_all_filters(collection: Collection[AlcoholFilter]) -> list[AlcoholFilter]:
        return list(collection.find().sort(key_or_list='_id'))

    @staticmethod
    async def create_init_entry(collection: Collection[AlcoholFilter], kind: str) -> None:
        collection.insert_one({'_id': kind, 'type': [], 'country': [], 'color': []})
