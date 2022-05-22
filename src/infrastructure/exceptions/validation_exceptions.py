from fastapi import HTTPException, status


class ValidationErrorException(HTTPException):
    def __init__(self, details: str):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            f'Invalid payload. \n {details}',
        )
