
import sys
from f_ai.argument_handler.arg_parsing import ArgumentHandler, ArgumentStatusCodes

CLI_TITLE = "F-AI CLI"


class CLI:
    def __init__(self, title=CLI_TITLE):
        self.title = title

    def start_command_factory(self, model_name: str, server_type: str):
        # we can have various mode-server types which will have different ways to start them
        # each type is mapped to a corresponding class that knows how to start it
        command_class = self.get_command_class_map().get((model_name, server_type))
        if command_class is None:
            raise ValueError(f"Unknown model-server type combination: {model_name}-{server_type}")

        command_object = command_class(model_name, server_type)

        return command_object

    def get_command_class_map(self):
        return {
            # ('parrot_fml', 'http'): Model1ServerType1Command,
        }

    def run(self, args: list):
        argument_handler = ArgumentHandler(args, self.title)
        status_code = argument_handler.handle_args(sys.argv)
        if status_code == ArgumentStatusCodes.EXIT_APPLICATION:
            sys.exit(0)

        # TODO: assuming we have a model name, should be checked in argument_handler
        model_name = argument_handler.args.model_name
        server_type = argument_handler.args.server_type

        command = self.start_command_factory(model_name, server_type)
        command.execute()

        print("Run not implemented. Exiting...")
        sys.exit(0)


def main():
    try:
        cli = CLI()
        cli.run(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nUser aborted!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
