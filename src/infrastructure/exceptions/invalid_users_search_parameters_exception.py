from fastapi import HTTPException, status


class InvalidUsersSearchParametersException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Niepoprawne parametry wyszukiwania'
        )
