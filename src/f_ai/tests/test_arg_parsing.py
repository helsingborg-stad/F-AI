import unittest
from argparse import Namespace
from f_ai.argument_handler.arg_parsing import ArgumentParserSetup, ArgumentHandler
from f_ai.version import __version__


class ArgumentParserSetupTest(unittest.TestCase):
    def test_init_and_setup(self):
        setup = ArgumentParserSetup('test_program')
        args = setup.parser.parse_args(['--version'])
        self.assertEqual(args.version, True)


class ArgumentHandlerTest(unittest.TestCase):
    def test_handle_args_no_args(self):
        handler = ArgumentHandler([], 'test_program')
        help_message = handler.handle_args([])
        self.assertIsNotNone(help_message)
        self.assertIn('test_program', help_message)

    def test_handle_args_version(self):
        handler = ArgumentHandler(['--version'], 'test_program')
        version_message = handler.handle_args(['test_program', '--version'])
        self.assertEqual(version_message, f"test_program {__version__}")


if __name__ == '__main__':
    unittest.main()
