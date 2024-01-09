from rich.console import Console
from rich.theme import Theme

console = Console(
    theme=Theme(
        {"logging.level.debug": "dim cyan", "warning": "magenta", "danger": "bold red"}
    )
)
