from typing import Collection


class MarkdownFormatter:

    @staticmethod
    def list_to_markdown(lst):
        return "\n".join(f"* {item}" for item in lst)

    @staticmethod
    def collection_to_markdown_table(header, collection):
        collection_as_list = list(collection)  # Convert collection to list
        header_line = f"| {header} |"
        separator = "|-" + "-" * len(header) + "-|"
        rows = "\n".join([f"| {item} |" for item in collection_as_list])
        return "\n".join([header_line, separator, rows])

    @staticmethod
    def code_block(language, code):
        return f"```{language}\n{code}\n```"

    @staticmethod
    def header(level, text):
        if not (1 <= level <= 6):
            raise ValueError("Header level must be between 1 and 6 inclusive.")
        return f"{'#' * level} {text}"
