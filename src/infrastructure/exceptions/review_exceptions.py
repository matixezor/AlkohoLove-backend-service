from fastapi import HTTPException, status


class AlcoholDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Alcohol not found'
        )


class WrongRatingFormat(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Rating should be number from 1 to 10'
        )


class ReviewAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review already exists'
        )


class ReviewDoesNotBelongToUser(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review does not belong to user'
        )


class ReviewNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review not found'
        )


class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'User not found'
        )
