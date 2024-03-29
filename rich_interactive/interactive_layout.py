from rich import box
from rich.console import RenderableType
from rich.layout import Layout

from rich_interactive.interactive import Interactive


class InteractiveLayout(Interactive, Layout):
    _selection_index: int = 0
    _parent: "InteractiveLayout" = None
    _selected_box: box.Box
    _selected_border_style: str

    def __init__(
        self,
        selected_box=box.HEAVY_EDGE,
        selected_border_style="bold bright_white",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._selected_box = selected_box
        self._selected_border_style = selected_border_style

    def split(self, *args, **kwargs):
        super().split(*args, **kwargs)
        self._refresh_parent_tree_structure()

    def add_split(self, *args, **kwargs):
        super().add_split(*args, **kwargs)
        self._refresh_parent_tree_structure()

    def split_row(self, *args, **kwargs):
        super().split_row(*args, **kwargs)
        self._refresh_parent_tree_structure()

    def split_column(self, *args, **kwargs):
        super().split_column(*args, **kwargs)
        self._refresh_parent_tree_structure()

    def unsplit(self, *args, **kwargs):
        super().unsplit(*args, **kwargs)
        self._refresh_parent_tree_structure()

    def _refresh_parent_tree_structure(self):
        for child in self.children:
            child._parent = self

            if isinstance(child, InteractiveLayout):
                child._refresh_parent_tree_structure()

    @property
    def descendants(self) -> list["InteractiveLayout"]:
        result = []

        for child in self.children:
            if isinstance(child, InteractiveLayout):
                result.extend(child.descendants)
            else:
                result.append(child.name)

        if not self.children:
            result.append(self)

        return result

    @property
    def top_layout(self):
        return self._parent.top_layout if self._parent else self

    @property
    def names(self) -> list[str]:
        return [d.name for d in self.descendants]

    @property
    def is_selected(self) -> bool:
        return self.top_layout._selection_index == self.top_layout.names.index(
            self.name
        )

    @property
    def renderable(self) -> RenderableType:
        result = super().renderable
        result.layout = self

        if self.is_selected and isinstance(result, Interactive):
            result.box = self._selected_box
            result.border_style = self._selected_border_style
        else:
            result.box = box.SQUARE

        return result

    @property
    def selected_layout_index(self):
        return self.top_layout._selection_index

    def selected_layout(self):
        return self.top_layout[self.names[self.selected_layout_index]]

    def switch_selection(self):
        if self._selection_index < len(self.names) - 1:
            self._selection_index += 1
        else:
            self._selection_index = 0

    def switch_selection_back(self):
        if self._selection_index > 0:
            self._selection_index -= 1
        else:
            self._selection_index = len(self.names) - 1


if __name__ == "__main__":
    from rich.console import Console
    from rich.text import Text
    from rich.syntax import Syntax
    from rich_interactive.interactive_panel import InteractivePanel as Panel
    from rich_interactive.interactive_layout import InteractiveLayout as Layout

    console = Console(width=60, height=15)
    print = console.print

    layout = Layout()
    layout.split(
        Layout(name="header", size=5),
        Layout(name="main", size=5),
        Layout(name="footer", size=5),
    )

    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))

    code = """
    from rich.console import Console
    from rich.text import Text

    from rich_interactive.interactive_panel import InteractivePanel as Panel
    from rich_interactive.interactive_layout import InteractiveLayout as Layout

    console = Console(width=60, height=15)

    layout = Layout()
    layout.split(
        Layout(name="header", size=5),
        Layout(name="main", size=5),
        Layout(name="footer", size=5),
    )

    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))

    print("Initial layout:")
    print(layout)

    layout.switch_selection()

    print("After switching selection:")
    print(layout)
    """

    print(Syntax(code, "python", dedent=True))
    print("Initial layout:")
    print(layout)
    print()

    layout.switch_selection()

    print("After switching selection:")
    print(layout)
