from pydantic import BaseModel

from fai_llm.serializer.impl.json import JSONSerializer


class MockModel(BaseModel):
    name: str
    description: str
    flag: bool
    value: int
    percentage: float


def test_json():
    serializer = JSONSerializer()

    mock_model = MockModel(
        name='ABC',
        description='DEFGH',
        flag=True,
        value=123,
        percentage=0.456,
    )

    result = serializer.serialize(mock_model)
    deserialized = serializer.deserialize(result, MockModel)

    assert result == '{"name":"ABC","description":"DEFGH","flag":true,"value":123,"percentage":0.456}'
    assert deserialized == mock_model
