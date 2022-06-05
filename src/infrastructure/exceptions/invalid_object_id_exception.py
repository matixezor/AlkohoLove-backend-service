from fastapi import HTTPException, status


class InvalidObjectIdException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'It is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'
        )
