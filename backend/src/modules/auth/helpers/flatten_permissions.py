from collections import defaultdict

from pydantic import BaseModel


class Resource(BaseModel):
    id: str
    scopes: list[str]


class Permissions(BaseModel):
    scopes: list[str]
    resources: list[Resource]


def flatten_permissions(groups: list[Permissions]) -> Permissions:
    all_scopes = list(set([scope for group in groups for scope in group.scopes]))

    all_resources = [resource for group in groups for resource in group.resources]

    resources_dict: dict[str, set] = defaultdict(set)

    for resource in all_resources:
        resources_dict[resource.id].update(resource.scopes)

    resources = [Resource(id=k, scopes=list(v)) for k, v in resources_dict.items()]

    return Permissions(scopes=all_scopes, resources=resources)
