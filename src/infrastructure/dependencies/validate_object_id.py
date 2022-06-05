from bson.objectid import ObjectId

from src.infrastructure.exceptions.invalid_object_id_exception import InvalidObjectIdException


def validate_object_ids(*args):
    return [ObjectId(arg) if ObjectId.is_valid(arg) else raise InvalidObjectIdException for arg in args]
