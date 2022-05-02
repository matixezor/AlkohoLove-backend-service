from fastapi import HTTPException, status


def raise_user_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
