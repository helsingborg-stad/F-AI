from pydantic import BaseModel

from fai_llm.serializer.impl.base64 import Base64Serializer


class MockModel(BaseModel):
    name: str
    description: str
    flag: bool
    value: int
    percentage: float


def test_base64():
    serializer = Base64Serializer[MockModel]()

    mock_model = MockModel(
        name='ABC',
        description='DEFGH',
        flag=True,
        value=123,
        percentage=0.456,
    )

    result = serializer.serialize(mock_model)
    deserialized = serializer.deserialize(result, MockModel)

    assert result == 'eyJuYW1lIjoiQUJDIiwiZGVzY3JpcHRpb24iOiJERUZHSCIsImZsYWciOnRydWUsInZhbHVlIjoxMjMsInBlcmNlbnRhZ2UiOjAuNDU2fQ=='
    assert deserialized == mock_model
