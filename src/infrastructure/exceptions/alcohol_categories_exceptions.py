from fastapi import HTTPException, status


class AlcoholCategoryExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Kategoria już istnieje.'
        )


class AlcoholCategoryNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Nie znaleziono kategorii.'
        )


class PropertiesAlreadyExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Podane cechy już istnieją.'
        )


class PropertiesNotExistException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Podane cechy nie istnieją.'
        )
