import unittest
from planning_permission.utils.command_registry import CommandRegistry
import unittest

class TestCommandRegistry(unittest.TestCase):
    def test_default_command(self):
        registry = CommandRegistry()
        registry.set_default_command(lambda input: f"Default command: {input}")
        
        @registry.command('existing_command')
        def existing_command() -> str:
            return "This is a existing command."
        
        self.assertEqual(registry.execute('Test'), "Default command: Test")

    def test_simple_command(self):
        registry = CommandRegistry()
        
        @registry.command('simple_command')
        def simple_command() -> str:
            return "This is a simple command."

        registry.set_default_command(lambda input: f"Default command: {input}")
        self.assertEqual(registry.execute('/simple_command'), "This is a simple command.")

    def test_command_with_one_arg(self):
        registry = CommandRegistry()

        @registry.command('command_with_one_arg')
        def command_with_one_arg(arg: str) -> str:
            return f"Arg: {arg}"

        self.assertEqual(registry.execute('/command_with_one_arg lol'), "Arg: lol")

    def test_command_with_many_args(self):
        registry = CommandRegistry()

        @registry.command('command_with_many_args')
        def command_with_many_args(arg1: int, arg2: int, arg3: int) -> str:
            return f"Sum: {arg1 + arg2 + arg3}"

        self.assertEqual(registry.execute('/command_with_many_args 2 2 2'), "Sum: 6")

    def test_command_with_bool_flag(self):
        registry = CommandRegistry()

        @registry.command('command_with_bool_flag')
        def command_with_bool_flag(boolean: bool = False) -> str:
            return "Has flag" if boolean else "No flag"

        self.assertEqual(registry.execute('/command_with_bool_flag'), "No flag")
        self.assertEqual(registry.execute('/command_with_bool_flag --boolean'), "Has flag")

    def test_command_with_value_flag(self):
        registry = CommandRegistry()

        @registry.command('command_with_value_flag')
        def command_with_flag(value: str = 'Default value') -> str:
            return f"Flag value: {value}"

        self.assertEqual(registry.execute('/command_with_value_flag'), "Flag value: Default value")
        self.assertEqual(registry.execute('/command_with_value_flag --value Flag'), "Flag value: Flag")

    def test_command_with_args_and_flags(self):
        registry = CommandRegistry()

        @registry.command('command_with_args_and_flags')
        def command_with_args_and_flags(name: str, age: int, phrase: str = 'Hello', min_age: int = 18) -> str:
            greet = f"{phrase}, {name}!"
            return f"{greet}, You must be at least {min_age} years old to use this command." if age < min_age else greet

        self.assertEqual(registry.execute('/command_with_args_and_flags Alice 17'), "Hello, Alice!, You must be at least 18 years old to use this command.")
        self.assertEqual(registry.execute('/command_with_args_and_flags Alice 19'), "Hello, Alice!")
        self.assertEqual(registry.execute('/command_with_args_and_flags Alice 19 --phrase Hi'), "Hi, Alice!")
        self.assertEqual(registry.execute('/command_with_args_and_flags Alice 19 --phrase Hi --min_age 20'), "Hi, Alice!, You must be at least 20 years old to use this command.")

    def test_unknown_command(self):
        registry = CommandRegistry()
        self.assertEqual(registry.execute('/unknown_command'), "Unknown command: unknown_command. Type /help for a list of commands.")

    def test_missing_required_arguments(self):
        registry = CommandRegistry()

        @registry.command('command_with_required_arg')
        def command_with_required_arg(arg: str) -> str:
            return f"{arg}"
        
        self.assertTrue("arg" in registry.execute('/command_with_required_arg'))
        self.assertTrue("required" in registry.execute('/command_with_required_arg'))
        self.assertTrue("arguments" in registry.execute('/command_with_required_arg'))

    def test_invalid_argument_type(self):
        registry = CommandRegistry()

        @registry.command('command_with_int_arg')
        def command_with_int_arg(arg: int) -> str:
            return f"{arg}"

        self.assertTrue("invalid int" in registry.execute('/command_with_int_arg string'))

if __name__ == '__main__':
   unittest.main()
        
    