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

    def traverse(self) -> list["InteractiveLayout"]:
        result = []

        for child in self.children:
            child._parent = self

            if isinstance(child, InteractiveLayout):
                result.extend(child.traverse())
            else:
                result.append(child.name)

        if not self.children:
            result.append(self.name)

        return result

    @property
    def top_layout(self):
        return self._parent.top_layout if self._parent else self

    @property
    def names(self) -> list[str]:
        return self.traverse()

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

    console = Console(width=60, height=15)
    print = console.print

    layout = InteractiveLayout()
    layout.split(
        InteractiveLayout(name="header", size=5),
        InteractiveLayout(name="main", size=5),
        InteractiveLayout(name="footer", size=5),
    )
    layout.traverse()
    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))

    code = """
    console = Console(width=60, height=15)

    layout = InteractiveLayout()
    layout.split(
        InteractiveLayout(name="header", size=5),
        InteractiveLayout(name="main", size=5),
        InteractiveLayout(name="footer", size=5),
    )
    layout.traverse()
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
