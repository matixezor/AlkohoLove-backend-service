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


class EmailNotVerifiedException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Email not verified'
        )


class InvalidVerificationCode(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f'Invalid verification code or account already verified'
        )


class InvalidChangePasswordCode(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail=f'Invalid change password code'
        )


class SendingEmailError(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'There was an error sending email'
        )


class InsufficientPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail=f'Insufficient permissions'
        )
