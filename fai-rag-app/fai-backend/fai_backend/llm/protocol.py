from typing import Protocol, AsyncGenerator

from langstream import Stream, StreamOutput


class ILLMProtocol(Protocol):
    def run(self, input_message: str) -> AsyncGenerator[StreamOutput[str], str]:
        """
        Takes an input message and returns an async stream resolving to the response from the LLM.

        :param input_message: The input message, as a string.
        :type input_message: str

        :return: The resulting `Stream[str, str]` object.
        :rtype: Stream[str, str]

        """
        ...
