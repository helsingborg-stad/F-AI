from pathlib import Path
from fastapi import HTTPException, Request
from starlette.responses import RedirectResponse

GIT_REVISION_FILE = 'git_revision.txt'


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


async def add_git_revision_to_request_header(request: Request, call_next) -> RedirectResponse:
    git_rev = read_git_revision_from_file(GIT_REVISION_FILE)
    response = await call_next(request)

    if git_rev:
        response.headers['x-git-revision'] = git_rev

    return response


def read_file_contents(file_path: str, mode: str) -> str:
    file = Path(__file__).parent / file_path
    with file.open(mode) as f:
        return f.read().rstrip()


def read_git_revision_from_file(file_path: str) -> str | None:
    try:
        return read_file_contents(file_path, mode='r')
    except FileNotFoundError:
        return None
