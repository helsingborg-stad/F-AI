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
    def __init__(self, args: list, title: str):
        self.parser = ArgumentParserSetup(title)
        self.args = self.parser.parse_args(args)
        self.title = title

    def handle_args(self, argv: list):
        if len(argv) < 2:
            print(self.parser.parser.format_help())
            exit(0)

        if self.args.version:
            print(f"{self.title} {__version__}")
            exit(0)
