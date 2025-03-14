def make_auth_path_description(path_description: str, scopes: list[str]) -> str:
    if len(scopes) == 0:
        return f'{path_description}\n\n*__(Auth) no scopes required__*'
    return f'{path_description}\n\n*__(Auth) required scope(s): {", ".join(scopes)}__*'
