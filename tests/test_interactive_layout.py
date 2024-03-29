from rich_interactive.interactive_layout import InteractiveLayout

from rich_interactive.interactive_panel import InteractivePanel as Panel
from rich.text import Text
from tests.utils import adjust_output as _
from tests.utils import diff_output


def get_layout():
    layout = InteractiveLayout(size=10)
    layout.split(
        InteractiveLayout(name="header", size=3),
        InteractiveLayout(name="main", size=3),
        InteractiveLayout(name="footer", size=3),
    )
    layout.traverse()
    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))
    return layout


def update_content(layout):
    index = layout.selected_layout_index
    layout["header"].update(Panel(Text(f"Selected layout: {index}", style="yellow")))

    return layout


def test_interactive_layout_default_layout_selection(render_to_text):
    layout = get_layout()
    update_content(layout)

    expected_output = _("""
    [1;97m┏━━━━━━━━━━━━━━━━━━━━┓[0m
    [1;97m┃[0m [33mSelected layout: 0[0m [1;97m┃[0m
    [1;97m┗━━━━━━━━━━━━━━━━━━━━┛[0m
    ┌────────────────────┐
    │ [33mmain[0m               │
    └────────────────────┘
    ┌────────────────────┐
    │ [33mfooter[0m             │
    └────────────────────┘
    """)

    output = render_to_text(layout, width=22, height=9)
    diff_output(output, expected_output)
