from fastapi import HTTPException, status


class ValidationErrorException(HTTPException):
    def __init__(self, details: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            f'Nieprawidłowe dane \n {details}',
        )
