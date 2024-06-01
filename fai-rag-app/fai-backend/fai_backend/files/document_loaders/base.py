import asyncio
from contextvars import copy_context
from functools import partial
from typing import Callable, ParamSpec, AsyncIterator, Iterator, Protocol, TypeVar, cast
from concurrent.futures import Executor

from fai_backend.files.documents import Document

P = ParamSpec("P")
T = TypeVar("T")


async def run_in_executor(executor: Executor | None,
                          func: Callable[P, T],
                          *args: P.args,
                          **kwargs: P.kwargs) -> T:
    return await asyncio.get_running_loop().run_in_executor(
        None,
        cast(Callable[..., T], partial(copy_context().run, func, *args, **kwargs)))


class IBaseLoader(Protocol):
    def load(self) -> list[Document]:
        return list(self.lazy_load())

    async def aload(self) -> list[Document]:
        return [doc async for doc in self.alazy_load()]

    def lazy_load(self) -> Iterator[Document]:
        if type(self).load != IBaseLoader.load:
            return iter(self.load())
        raise NotImplemented(f'{self.__class__.__name__} does not implement lazy_load()')

    async def alazy_load(self) -> AsyncIterator[Document]:
        iterator = await run_in_executor(None, self.lazy_load)
        done = object()
        while True:
            doc = await run_in_executor(None, next, iterator, done)
            if doc is done:
                break
            yield doc
