from fastapi import HTTPException, status


class ReportedErrorNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Zgłoszony błąd nie znaleziony.'
        )
