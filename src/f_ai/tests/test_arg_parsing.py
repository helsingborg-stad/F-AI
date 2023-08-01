import unittest
from f_ai.argument_handler.arg_parsing import ArgumentParserSetup, ArgumentHandler, ArgumentStatusCodes
from f_ai.version import __version__


class ArgumentParserSetupTest(unittest.TestCase):
    def test_init_and_setup(self):
        setup = ArgumentParserSetup('test_program')
        args = setup.parser.parse_args(['--version'])
        self.assertEqual(args.version, True)


class ArgumentHandlerTest(unittest.TestCase):
    def test_handle_args_no_args(self):
        handler = ArgumentHandler([], 'test_program')
        arg_status_code = handler.handle_args([])
        self.assertEqual(arg_status_code, ArgumentStatusCodes.EXIT_APPLICATION)

    def test_handle_args_version(self):
        handler = ArgumentHandler(['--version'], 'test_program')
        arg_status_code = handler.handle_args(['test_program', '--version'])
        self.assertEqual(arg_status_code, ArgumentStatusCodes.EXIT_APPLICATION)


if __name__ == '__main__':
    unittest.main()
