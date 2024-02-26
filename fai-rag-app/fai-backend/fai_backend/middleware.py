from fastapi import HTTPException, Request
from starlette.responses import RedirectResponse


async def remove_trailing_slash(request: Request, call_next):
    path = str(request.url.path)
    if len(path) > 1 and path.endswith('/'):
        if request.method in ['GET', 'HEAD']:
            new_path = path.rstrip('/')
            if request.query_params:
                new_path += f'?{request.query_params}'
            return RedirectResponse(url=new_path, status_code=301)
        else:
            raise HTTPException(
                status_code=307, detail='Trailing slash on non-GET request not allowed'
            )
    response = await call_next(request)
    return response
