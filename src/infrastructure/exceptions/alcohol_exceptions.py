from fastapi import HTTPException, status


class AlcoholExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Alkohol już istnieje.'
        )


class AlcoholNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            'Nie znaleziono alkoholu.'
        )


class NoBarcodeException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Należy podać kod kreskowy.'
        )


class WrongFileTypeException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Dozwolone jedynie pliki .png i .jpg.'
        )


class FileTooBigException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            'Za duży rozmiar pliku. Maksymalny rozmiar to 1 mb.'
        )
