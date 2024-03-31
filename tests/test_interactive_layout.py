from rich import box
from rich.text import Text

from rich_interactive.interactive_layout import InteractiveLayout
from rich_interactive.interactive_panel import InteractivePanel as Panel
from tests.utils import adjust_output as _
from tests.utils import diff_output


def get_layout(*args, **kwargs):
    layout = InteractiveLayout(size=10, *args, **kwargs)
    layout.split(
        InteractiveLayout(name="header", size=3),
        InteractiveLayout(name="main", size=3),
        InteractiveLayout(name="footer", size=3),
    )

    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))
    return layout


def update_content(layout):
    index = str(layout.selected_layout_index)
    layout["header"].update(Panel(Text(f"Selected layout: {index}", style="yellow")))

    return layout


def test_interactive_layout__default_layout_selection(render_to_text):
    layout = get_layout()
    update_content(layout)

    expected_output = _("""
    [1;97m┏━━━━━━━━━━━━━━━━━━━━┓[0m
    [1;97m┃[0m [33mSelected layout: 0[0m [1;97m┃[0m
    [1;97m┗━━━━━━━━━━━━━━━━━━━━┛[0m
    ╭────────────────────╮
    │ [33mmain[0m               │
    ╰────────────────────╯
    ╭────────────────────╮
    │ [33mfooter[0m             │
    ╰────────────────────╯
    """)

    output = render_to_text(layout, width=22, height=9)
    diff_output(output, expected_output)


def test_interactive_layout__restores_box_and_box_style_to_original_after_selection_is_removed(
    render_to_text,
):
    layout = get_layout(selected_border_style="bold red", selected_box=box.ASCII2)
    output = render_to_text(layout, width=25, height=9)
    update_content(layout)
    expected_output = _("""
    [1;31m+-----------------------+[0m
    [1;31m|[0m [33mSelected layout: 0[0m    [1;31m|[0m
    [1;31m+-----------------------+[0m
    ╭───────────────────────╮
    │ [33mmain[0m                  │
    ╰───────────────────────╯
    ╭───────────────────────╮
    │ [33mfooter[0m                │
    ╰───────────────────────╯
    """)
    output = render_to_text(layout, width=25, height=9)
    diff_output(output, expected_output)

    layout.remove_selection()
    update_content(layout)

    expected_output = _("""
    ╭───────────────────────╮
    │ [33mSelected layout: None[0m │
    ╰───────────────────────╯
    ╭───────────────────────╮
    │ [33mmain[0m                  │
    ╰───────────────────────╯
    ╭───────────────────────╮
    │ [33mfooter[0m                │
    ╰───────────────────────╯
    """)
    output = render_to_text(layout, width=25, height=9)
    diff_output(output, expected_output)
