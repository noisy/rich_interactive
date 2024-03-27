from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table

from rich_interactive.interactive import Interactive


class InteractiveTable(Interactive, Table):
    selected_row = 0
    is_selected: bool = False

    def get_row_style(self, console: Console, index: int) -> StyleType:
        style = super().get_row_style(console, index)

        if index == self.selected_row:
            style = style + Style(bgcolor="bright_red", color="white")

        return style

    @property
    def is_selected(self) -> bool:
        return not self.layout or self.layout.is_selected

    def move_selection_down(self):
        if self.selected_row < len(self.rows) - 1:
            self.selected_row += 1

    def move_selection_up(self):
        if self.selected_row > 0 and len(self.rows) > 0:
            self.selected_row -= 1
