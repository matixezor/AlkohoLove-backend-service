from bson.objectid import ObjectId

from src.infrastructure.exceptions.invalid_object_id_exception import InvalidObjectIdException


def validate_object_ids(*args):
    id_list = [ObjectId(arg) for arg in args if ObjectId.is_valid(arg)]
    if len(args) == len(id_list):
        return id_list
    else:
        raise InvalidObjectIdException
