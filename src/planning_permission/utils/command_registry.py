import argparse
import shlex
from typing import Any, Callable, Dict
from difflib import get_close_matches
from planning_permission.utils.terminal_input import user_input

class ErrorCatchingArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if status:
            raise Exception(message)
        exit(status)

class CommandRegistry:
    def __init__(self, exit_on_error = False):
        self.commands = {}
        self.default_command = None
        self._exit_on_error = exit_on_error
        
    def command(self, name: str):
        def decorator(func: Callable):
            parser = ErrorCatchingArgumentParser(prog=name, add_help=False, exit_on_error=self._exit_on_error)
            param_names = func.__code__.co_varnames[:func.__code__.co_argcount]
            param_defaults = func.__defaults__ or ()
            defaults_dict = dict(zip(param_names[-len(param_defaults):], param_defaults))

            for param, param_type in func.__annotations__.items():
                if param == "return":  # Ignore return type annotation
                    continue
                if param_type == bool:
                    if defaults_dict.get(param, False):
                        parser.add_argument(f'--{param}', dest=param, action='store_false')
                    else:
                        parser.add_argument(f'--{param}', dest=param, action='store_true')
                elif param in defaults_dict:
                    parser.add_argument(f'--{param}', dest=param, type=param_type, default=defaults_dict[param])
                else:
                    parser.add_argument(param, type=param_type)

            self.commands[name.lower()] = {'function': func, 'parser': parser}
            return func
        return decorator

    def set_default_command(self, func: Callable):
        self.default_command = func

    def execute(self, command_string: str) -> str:
        if not command_string.startswith('/'):
            if self.default_command:
                return self.default_command(command_string)
            return "Invalid command format. Commands should start with '/'."

        tokens = shlex.split(command_string[1:])
        command_name = tokens[0].lower()  # Case-insensitive command names
        command_args = tokens[1:]

        if command_name == "help":
            return self._generate_help_text()

        command = self.commands.get(command_name)
        if not command:
            suggestion = self._get_command_suggestion(command_name)
            suggestion_text = f" Did you mean '{suggestion}'?" if suggestion else ""
            return f"Unknown command: {command_name}. Type /help for a list of commands.{suggestion_text}"

        try:
            parsed_args = command['parser'].parse_args(command_args)
            return command['function'](**vars(parsed_args))
        except Exception as e:
            return str(e)

    def _generate_help_text(self) -> str:
        help_texts = ["Available commands:\n"]
        for command_name, command_data in self.commands.items():
            usage = command_data['parser'].format_usage()
            help_texts.append(f"/{command_name}{usage.replace('usage: ', '').replace(command_name, '')}")
        return "\n".join(help_texts)

    def _get_command_suggestion(self, command_name: str) -> str:
        """Get the closest matching command name if a user mistypes a command."""
        matches = get_close_matches(command_name, self.commands.keys(), n=1, cutoff=0.7)
        return matches[0] if matches else None

if __name__ == '__main__':
   registry = CommandRegistry()
   
   @registry.command('add') # Register command with python decorator syntax
   def add(a: int, b: int) -> str:
       return a + b
   
   @registry.command('greet')
   def greet(name: str, phrase: str = "Hello") -> str:
       return f"{phrase}, {name}!"
   
   registry.command('hi')(greet)  # Alternative syntax
   
   def default_command(msg: str):
       if msg == 'exit':
           raise KeyboardInterrupt() # Exit
       return 'Type "/help" to view commands or "exit" to exit.'
   
   registry.default_command = default_command
   
   while True: 
       try:
           print(registry.execute(user_input("Enter command: ")))
       except(EOFError, KeyboardInterrupt):
           print("Exiting...")
           exit(0)