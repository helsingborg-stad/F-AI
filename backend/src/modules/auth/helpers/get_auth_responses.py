import copy

from pydantic import BaseModel


class CommonHTTPErrorResponse(BaseModel):
    detail: str


_auth_responses = {
    400: {
        "description": "* (Auth) too many credentials provided; only one type should be used.",
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Too many authentication credentials provided (x+y)"
                )
            }
        }
    },
    401: {
        "description": '''No credentials provided or provided credentials are invalid (e.g. expired).
                        \nAvailable authentication methods are provided in the WWW-Authenticate header.''',
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Not Authenticated"
                )
            }
        }

    },
    403: {
        "description": "Credentials are missing one or more required scopes (operation permissions).",
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Missing one or more required scopes (x, y, z)"
                )
            }
        }
    },
}


def get_auth_responses(
        additional_400_description: str | None = None,
        optional_404_description: str | None = None
) -> dict[int, dict]:
    result = copy.deepcopy(_auth_responses)

    if additional_400_description:
        result[400]["description"] = f"One of:\n\n* {additional_400_description}\n{_auth_responses[400]['description']}"

    if optional_404_description:
        result[404] = {
            "description": optional_404_description,
            "model": CommonHTTPErrorResponse,
            "content": {"application/json": {"example": CommonHTTPErrorResponse(detail="Not Found")}}
        }

    return result
