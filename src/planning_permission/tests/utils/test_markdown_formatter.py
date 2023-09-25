import unittest

from planning_permission.utils.markdown import MarkdownFormatter


class TestMarkdownFormatter(unittest.TestCase):

    def test_list_to_markdown(self):
        lst = ["apple", "banana", "cherry"]
        expected = "* apple\n* banana\n* cherry"
        result = MarkdownFormatter.list_to_markdown(lst)
        self.assertEqual(result, expected)

    def test_collection_to_markdown_table_with_set(self):
        header = "Numbers"
        collection = {1, 2, 3}
        result = MarkdownFormatter.collection_to_markdown_table(header, collection)
        # Note: Sets are unordered, so we just check for existence of a row, not exact ordering.
        self.assertTrue("| 1 |" in result)
        self.assertTrue("| 2 |" in result)
        self.assertTrue("| 3 |" in result)

    def test_collection_to_markdown_table_with_custom_collection(self):
        header = "Letters"

        # Creating a custom 'Collection' class as an example
        class Collection:
            def __iter__(self):
                return iter(["a", "b", "c"])

        collection = Collection()
        result = MarkdownFormatter.collection_to_markdown_table(header, collection)
        expected = "| Letters |\n|---------|\n| a |\n| b |\n| c |"
        self.assertEqual(result, expected)

    def test_code_block(self):
        language = "python"
        code = "print('Hello, world!')"
        expected = "```python\nprint('Hello, world!')\n```"
        result = MarkdownFormatter.code_block(language, code)
        self.assertEqual(result, expected)

    def test_header(self):
        level = 3
        text = "This is a header"
        expected = "### This is a header"
        result = MarkdownFormatter.header(level, text)
        self.assertEqual(result, expected)

        # Test for valid header levels
        with self.assertRaises(ValueError):
            MarkdownFormatter.header(0, "Invalid header")
        with self.assertRaises(ValueError):
            MarkdownFormatter.header(7, "Invalid header")


if __name__ == '__main__':
    unittest.main()
