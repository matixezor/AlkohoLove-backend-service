from fastapi import HTTPException, status


class AlcoholAlreadyInListException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alcohol already in list'
        )
