from src.modules.auth.helpers.flatten_permissions import Permissions, Resource, flatten_permissions


def test_flatten_permissions():
    source = [
        Permissions(scopes=['can_read_x'], resources=[]),
        Permissions(scopes=['can_write_x'], resources=[]),
        Permissions(scopes=['can_read_x'], resources=[
            Resource(id='resource_a', scopes=['read'])
        ]),
        Permissions(scopes=['can_read_y'], resources=[
            Resource(id='resource_a', scopes=['write']),
            Resource(id='resource_b', scopes=['write'])
        ]),
        Permissions(scopes=[], resources=[
            Resource(id='resource_c', scopes=['read'])
        ]),
    ]

    expected = Permissions(
        scopes=['can_read_x', 'can_write_x', 'can_read_y'],
        resources=[
            Resource(id='resource_a', scopes=['read', 'write']),
            Resource(id='resource_b', scopes=['write']),
            Resource(id='resource_c', scopes=['read']),
        ]
    )

    result = flatten_permissions(source)

    assert frozenset(result.scopes) == frozenset(expected.scopes)
    assert [r.id for r in result.resources] == [r.id for r in expected.resources]
    for r in result.resources:
        assert frozenset(r.scopes) == frozenset(next(er for er in expected.resources if er.id == r.id).scopes)
