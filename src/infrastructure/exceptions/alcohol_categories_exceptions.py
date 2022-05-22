from fastapi import HTTPException, status


class AlcoholCategoryExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alcohol category exists'
        )
