from bson.objectid import ObjectId

from src.infrastructure.exceptions.invalid_object_id_exception import InvalidObjectIdException


def validate_object_id(object_id: str):
    if ObjectId.is_valid(object_id):
        return ObjectId(object_id)
    else:
        raise InvalidObjectIdException(object_id)
