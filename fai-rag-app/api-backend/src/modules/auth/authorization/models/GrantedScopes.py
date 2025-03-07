from pydantic import BaseModel


class GrantedScopes(BaseModel):
    global_scopes: list[str]
