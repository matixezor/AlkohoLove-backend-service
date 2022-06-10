from fastapi import HTTPException, status


class TagDoesNotBelongToUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Tag does not belong to user'
        )


class TagNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Tag not found'
        )


class TagAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Tag already exists'
        )


class AlcoholIsInTagException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alcohol already is in tag'
        )


class AlcoholDoesNotExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Alcohol not found'
        )
