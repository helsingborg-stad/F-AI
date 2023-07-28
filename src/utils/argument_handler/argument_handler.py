from argparse import ArgumentParser
from f_ai.version import __version__


class ArgumentHandler:
    def __init__(self, parser: ArgumentParser, args: list):
        self.parser = parser
        self.args = args

    def setup_parser(self):
        self.parser.add_argument('--version', action='store_true', help='Print version and exit')

    def parse_args(self):
        return self.parser.parse_args(self.args)

    def get_argument(self, name):
        return self.args[name]

    def get_argument_or_default(self, name, default):
        return self.args[name] if name in self.args else default

    def get_argument_or_error(self, name):
        if name not in self.args:
            raise Exception(f"Argument '{name}' is missing")
        return self.args[name]

    def get_argument_or_error_with_default(self, name, default):
        return self.args[name] if name in self.args else default

