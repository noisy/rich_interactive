from rich import box
from rich.console import RenderableType
from rich.layout import Layout

from rich_interactive.interactive import Interactive


class InteractiveLayout(Interactive, Layout):
    _selection_index: int | None = 0
    _parent: "InteractiveLayout" = None
    _selected_box: box.Box
    _selected_border_style: str

    DEFAULT_SELECTED_BOX: box.Box = box.HEAVY_EDGE
    DEFAULT_SELECTED_BORDER_STYLE: str = "bold bright_white"

    def __init__(
        self,
        selected_box=None,
        selected_border_style=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._selected_box = selected_box
        self._selected_border_style = selected_border_style

    def split(self, *args, **kwargs):
        super().split(*args, **kwargs)
        self.top_layout._refresh_parent_tree_structure()

    def add_split(self, *args, **kwargs):
        super().add_split(*args, **kwargs)
        self.top_layout._refresh_parent_tree_structure()

    def split_row(self, *args, **kwargs):
        super().split_row(*args, **kwargs)
        self.top_layout._refresh_parent_tree_structure()

    def split_column(self, *args, **kwargs):
        super().split_column(*args, **kwargs)
        self.top_layout._refresh_parent_tree_structure()

    def unsplit(self, *args, **kwargs):
        super().unsplit(*args, **kwargs)
        self.top_layout._refresh_parent_tree_structure()

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
        return self.top_layout._selection_index == self.top_layout.names.index(self.name)

    @property
    def renderable(self) -> RenderableType:
        result = super().renderable
        result.layout = self

        if self.is_selected and isinstance(result, Interactive):
            if not (hasattr(result, "original_box") or hasattr(result, "original_border_style")):
                result.original_box = result.box
                result.box = self.get_selected_box()

                result.original_border_style = result.border_style
                result.border_style = self.get_selected_border_style()
        else:
            if hasattr(result, "original_border_style"):
                result.border_style = result.original_border_style

            if hasattr(result, "original_box"):
                result.box = result.original_box

        return result

    def get_selected_border_style(self):
        if self._selected_border_style:
            return self._selected_border_style
        else:
            if self._parent:
                return self._parent.get_selected_border_style()
            else:
                return self.DEFAULT_SELECTED_BORDER_STYLE

    def get_selected_box(self):
        if self._selected_box:
            return self._selected_box
        else:
            if self._parent:
                return self._parent.get_selected_box()
            else:
                return self.DEFAULT_SELECTED_BOX

    @property
    def selected_layout_index(self):
        return self.top_layout._selection_index

    def selected_layout(self):
        return self.top_layout[self.names[self.selected_layout_index]]

    def switch_selection(self):
        if self._selection_index is None:
            if len(self.names) > 0:
                self._selection_index = 0
            else:
                return
        else:
            if self._selection_index < len(self.names) - 1:
                self._selection_index += 1
            else:
                self._selection_index = 0

    def switch_selection_back(self):
        if self._selection_index is None:
            if len(self.names) > 0:
                self._selection_index = len(self.names) - 1
            else:
                return
        else:
            if self._selection_index > 0:
                self._selection_index -= 1
            else:
                self._selection_index = len(self.names) - 1

    def remove_selection(self):
        self._selection_index = None


if __name__ == "__main__":
    from rich.console import Console
    from rich.text import Text

    from rich_interactive.interactive_layout import InteractiveLayout as Layout
    from rich_interactive.interactive_panel import InteractivePanel as Panel

    console = Console(width=60, height=15)
    print = console.print

    layout = Layout(selected_border_style="bold blue", selected_box=box.HEAVY_EDGE, size=15)
    layout.split(
        Layout(name="header", size=5),
        Layout(name="main", size=5),
        Layout(name="footer", size=5),
    )

    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))

    print("Initial layout:")
    print(layout)
    print()

    layout.switch_selection()

    print("After switching selection:")
    print(layout)
