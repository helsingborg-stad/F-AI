import sys
from f_ai.argument_handler.arg_parsing import ArgumentHandler

CLI_TITLE = "F-AI CLI"


class CLI:
    def __init__(self, title=CLI_TITLE):
        self.title = title

    def run(self, args: list):
        argument_handler = ArgumentHandler(args, self.title)
        status_code = argument_handler.handle_args(sys.argv)
        if status_code == ArgumentStatusCodes.EXIT_APPLICATION:
            sys.exit(0)

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
