from fastapi import HTTPException, status


class ReviewAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review already exists'
        )


class ReviewIsInappropriateException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review does not follow AlkohoLove standards'
        )


class ReviewDoesNotBelongToUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Review does not belong to user'
        )


class ReviewNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Review not found'
        )


class ReviewAlreadyReportedExcepiton(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'User already reported review'
        )


class OwnReviewAsHelpfulException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Can\'t mark/unmark own review as helpful'
        )
