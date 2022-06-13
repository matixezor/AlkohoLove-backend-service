from fastapi import HTTPException, status


class SuggestionAlreadyMadeException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'User already made a suggestion for this alcohol'
        )
