from fastapi import HTTPException, status


class TagDoesNotBelongToUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Tag nie należy do tego użytkownika.'
        )


class TagNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Nie znaleziono tagu.'
        )


class TagAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Taki tag już istnieje.'
        )


class AlcoholIsInTagException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alkohol należy już do tego tagu.'
        )
