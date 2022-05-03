from fastapi import HTTPException, status


def raise_reported_error_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reported error not found')
