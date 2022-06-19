from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Could not validate credentials',
            {'WWW-Authenticate': 'Bearer'}
        )


class UserBannedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            'Access denied. User is banned',
        )


class TokenRevokedException(HTTPException):
    def __init__(self, token_type):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            f'{token_type} token is blacklisted',
        )


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid username or password'
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Insufficient permissions'
        )
