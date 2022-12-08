from fastapi import HTTPException, status


class SuggestionAlreadyMadeException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Użytkownik już dodał sugestię dla tego alkoholu.'
        )


class SuggestionNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Nie znaleziono sugestii.'
        )


class WrongSuggestionFileTypeException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Dozwolone jedynie pliki .png i .jpg.'
        )


class SuggestionFileTooBigException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Za duży rozmiar pliku. Maksymalny rozmiar to 9 mb.'
        )
