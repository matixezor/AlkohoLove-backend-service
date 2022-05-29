from fastapi import HTTPException, status


class UserAlreadyInFollowedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'This user is already in following'
        )


class UserAlreadyInFollowersException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'This user is already in followers'
        )
