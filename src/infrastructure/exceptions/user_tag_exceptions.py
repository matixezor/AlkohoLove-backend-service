from fastapi import HTTPException, status


class TagDoesNotBelongToUser(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Tag does not belong to user'
        )


class TagNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Tag not found'
        )


class TagAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Tag already exists'
        )


class AlcoholIsInTag(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alcohol already is in tag'
        )


class AlcoholDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Alcohol not found'
        )
