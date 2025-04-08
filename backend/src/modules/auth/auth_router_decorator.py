import inspect
from collections.abc import Callable
from functools import partial
from typing import Any

from fastapi import APIRouter, Security

from src.modules.auth.helpers.auth_route_dependency import auth_route_dependency
from src.modules.auth.helpers.get_auth_responses import get_auth_responses
from src.modules.auth.helpers.make_auth_path_description import make_auth_path_description


class AuthRouterDecorator:
    def __init__(self, api_router: APIRouter):
        self.api_router = api_router

    @staticmethod
    def route(
            router_method: Callable,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        if required_scopes is None:
            required_scopes = []

        responses = get_auth_responses(response_400_description, response_404_description)

        def inner_decorator(func):
            security_dependency = Security(auth_route_dependency, scopes=required_scopes)
            parameters = inspect.signature(func).parameters
            function_has_identity_parameter = 'auth_identity' in parameters
            fn = partial(func,
                         auth_identity=security_dependency) if function_has_identity_parameter else func
            deps = [] if function_has_identity_parameter else [security_dependency]

            router_method(
                path,
                summary=summary,
                description=make_auth_path_description(description or '', scopes=required_scopes),
                response_model=response_model,
                response_description=response_description,
                responses=responses,
                dependencies=deps,
                status_code=status_code,
            )(fn)

        return inner_decorator

    def get(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.get,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            response_404_description=response_404_description,
            status_code=status_code,
        )

    def post(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.post,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            response_404_description=response_404_description,
            status_code=status_code,
        )

    def put(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.put,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            response_404_description=response_404_description,
            status_code=status_code,
        )

    def patch(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.patch,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            response_404_description=response_404_description,
            status_code=status_code,
        )

    def delete(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            response_404_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.delete,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            response_404_description=response_404_description,
            status_code=status_code,
        )
