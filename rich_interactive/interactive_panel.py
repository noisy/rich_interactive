from rich.panel import Panel

from rich_interactive.interactive import Interactive


class InteractivePanel(Interactive, Panel):
    scrollable: bool

    def __init__(self, *args, scrollable: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.scrollable = scrollable
