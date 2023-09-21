class MarkdownFormatter:

    @staticmethod
    def list_to_markdown(lst):
        return "\n".join(f"* {item}" for item in lst)

    @staticmethod
    def list_to_markdown_table(header, lst):
        header_line = f"| {header} |"
        separator = "|-" + "-" * len(header) + "-|"
        rows = "\n".join([f"| {item} |" for item in lst])
        return "\n".join([header_line, separator, rows])

    @staticmethod
    def code_block(language, code):
        return f"```{language}\n{code}\n```"

    @staticmethod
    def header(level, text):
        return f"{'#' * level} {text}"
