from fastapi import HTTPException, status


class ReviewAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Opinia już istnieje.'
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
            'Opinia nie należy do tego użytkownika.'
        )


class ReviewNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Opinia nie znaleziona.'
        )


class ReviewAlreadyReportedExcepiton(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Opinia została już dodana przez tego użytkownika.'
        )


class OwnReviewAsHelpfulException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Nie można oznaczyć swojej opinii jako pomocna.'
        )


class WrongRatingValueException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Ocena powinna być cyfrą od 1 do 5.'
        )
