# arg_parsing.py
import sys
from argparse import ArgumentParser, Namespace
from f_ai.version import __version__


class ArgumentParserSetup:
    def __init__(self, title: str):
        self.parser = ArgumentParser(prog=title)
        self.setup_parser()

    def setup_parser(self):
        self.parser.add_argument('--version', action='store_true', help='Print version and exit')

    def parse_args(self, args: list) -> Namespace:
        return self.parser.parse_args(args)


class ArgumentHandler:
    def __init__(self, args: Namespace, parser: ArgumentParser, title: str):
        self.args = args
        self.parser = parser
        self.title = title
        self.handle_args()

    def handle_args(self):
        if len(sys.argv) < 2:
            self.parser.print_help()
            sys.exit(0)
        if self.args.version:
            print(f"{self.title} {__version__}")
            sys.exit(0)
