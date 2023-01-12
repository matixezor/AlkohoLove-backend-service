from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Uwierzytelnienie nie powiodło się.',
            {'WWW-Authenticate': 'Bearer'}
        )


class UserBannedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Brak dostępu. Użytkownik jest zablokowany.',
        )


class TokenRevokedException(HTTPException):
    def __init__(self, token_type):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            f'{token_type} token jest na czarnej liście.',
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Nieprawidłowa nazwa użytkownika lub hasło.'
        )


class EmailNotVerifiedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Adres mailowy nie jest zweryfikowany.'
        )


class InvalidVerificationCode(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f'Nieprawidłowy kod weryfikacji lub konto już zweryfikowane.'
        )


class InvalidChangePasswordCode(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f'Nieprawidłowy kod zmiany hasła.'
        )


class SendingEmailError(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Błąd przy wysyłaniu maila.'
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f'Niewystarczające uprawnienia.'
        )


class PasswordNotProvidedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Oba hasła muszą zostać podane.'
        )


class IncorrectOldPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'Stare hasło jest niepoprawne.'
        )


class IncorrectPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Hasło nie spełnia zasad.',
        )


class IncorrectEmailException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            'Nieprawidłowy email.',
        )
