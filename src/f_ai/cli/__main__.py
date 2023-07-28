# main.py

import sys
from f_ai.argument_handler.arg_parsing import ArgumentParserSetup, ArgumentHandler

CLI_TITLE = "F-AI CLI"

class CLI:
    def __init__(self, title=CLI_TITLE):
        self.title = title

    def run(self, args: list):
        parser_setup = ArgumentParserSetup(self.title)
        parsed_args = parser_setup.parse_args(args)
        ArgumentHandler(parsed_args, parser_setup.parser, self.title)
        print("Run not implemented. Exiting...")
        sys.exit(0)


def main():
    try:
        cli = CLI()
        cli.run(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nUser aborted!")
        sys.exit(0)


if __name__ == '__main__':
    main()
