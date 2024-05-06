from fastapi import HTTPException, status
from functools import wraps


def handle_errors(f):
    @wraps(f)
    async def decorator(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
        except KeyError as ke:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found: " + str(ke)
            )
        except Exception as e:
            # Log exception details here if logging is set up
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal server error occurred."
            )

    return decorator
