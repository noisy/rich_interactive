from rich.console import Console
from rich.style import Style, StyleType
from rich.table import Table

from rich_interactive.interactive import Interactive


class InteractiveTable(Interactive, Table):
    selected_row: int | None = None
    is_selected: bool = False
    rotate_selection: bool = False

    def __init__(self, selected_row=0, rotate_selection=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_row = selected_row
        self.rotate_selection = rotate_selection

    def get_row_style(self, console: Console, index: int) -> StyleType:
        style = super().get_row_style(console, index)

        if index == self.selected_row:
            style = style + Style(bgcolor="bright_black", color="white")

        return style

    @property
    def is_selected(self) -> bool:
        return not self.layout or self.layout.is_selected

    def move_selection_down(self):
        if self.selected_row is None and len(self.rows) > 0:
            self.selected_row = 0

        if self.selected_row < len(self.rows) - 1:
            self.selected_row += 1

        if self.selected_row == len(self.rows) - 1 and self.rotate_selection:
            self.selected_row = 0

    def move_selection_up(self):
        if self.selected_row is None and len(self.rows) > 0:
            self.selected_row = len(self.rows) - 1

        if self.selected_row > 0 and len(self.rows) > 0:
            self.selected_row -= 1

        if self.selected_row == 0 and self.rotate_selection:
            self.selected_row = len(self.rows) - 1
