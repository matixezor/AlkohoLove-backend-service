from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Nie znaleziono użytkownika.',
        )


class UserExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Taki użytkownik już istnieje.',
        )


class NoValuesProvidedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Przynajmniej jedna z wartości musi zostać podana.',
        )
