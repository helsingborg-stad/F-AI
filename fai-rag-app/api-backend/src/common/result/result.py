import asyncio
from dataclasses import dataclass
from typing import TypeVar, Generic

TValue = TypeVar('TValue')
TError = TypeVar('TError')


class Result(Generic[TValue, TError]):
    pass


@dataclass
class Ok(Result[TValue, TError]):
    value: TValue


@dataclass
class Error(Result[TValue, TError]):
    error: TError


if __name__ == '__main__':
    async def some_func(num: int) -> Result[str, ValueError]:
        await asyncio.sleep(0.1)
        if num == 0:
            return Ok('zero')
        return Error(ValueError('non-zero not supported bro'))


    async def main():
        result1 = await some_func(0)
        result2 = await some_func(1)

        match result1:
            case Ok(value):
                print(f'1 is OK: ({type(result1)} {type(value)}) {value}')
            case Error(value):
                print(f'1 is ERROR: ({type(result1)} {type(value)}) {value}')

        match result2:
            case Ok(value):
                print(f'2 is OK: ({type(result2)} {type(value)}) {value}')
            case Error(value):
                print(f'2 is ERROR: ({type(result2)} {type(value)}) {value}')


    asyncio.run(main())
