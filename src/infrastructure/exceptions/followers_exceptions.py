from fastapi import HTTPException, status


class UserAlreadyInFollowingException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Ten użytkownik jest już w obserwowanych.'
        )


class UserAlreadyInFollowersException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Ten użytkownik jest już w obserwujących.'
        )
