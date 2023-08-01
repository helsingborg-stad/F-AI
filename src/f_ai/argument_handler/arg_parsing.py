from argparse import ArgumentParser, Namespace
from enum import Enum

from f_ai.version import __version__


class ArgumentParserSetup:
    def __init__(self, title: str):
        self.parser = ArgumentParser(prog=title)
        self.setup_parser()

    def setup_parser(self):
        self.parser.add_argument('--version', action='store_true', help='Print version and exit')
        self.parser.add_argument('--server-type', type=str, default='http', help='Server type to run')
        self.parser.add_argument('--model_name', type=str, help='Name of the model to run')

    def parse_args(self, args: list) -> Namespace:
        return self.parser.parse_args(args)


class ArgumentStatusCodes(Enum):
    EXIT_APPLICATION = 0
    CONTINUE = 1


class ArgumentHandler:
    def __init__(self, args: list, title: str):
        self.parser = ArgumentParserSetup(title)
        self.args = self.parser.parse_args(args)
        self.title = title

    def handle_args(self, argv: list) -> ArgumentStatusCodes:
        if len(argv) < 2:
            print(self.parser.parser.format_help())
            return ArgumentStatusCodes.EXIT_APPLICATION

        if self.args.version:
            print(f"{self.title} {__version__}")
            return ArgumentStatusCodes.EXIT_APPLICATION

        return ArgumentStatusCodes.CONTINUE
