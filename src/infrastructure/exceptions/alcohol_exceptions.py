from fastapi import HTTPException, status


class AlcoholExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alcohol exists'
        )


class AlcoholNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Alcohol not found'
        )
