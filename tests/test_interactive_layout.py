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


def test_default_layout_selection(render_to_text):
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


def test_restores_box_and_box_style_to_original_after_selection_is_removed(
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


def test_box_and_box_style_is_derived_from_parent_if_not_set(render_to_text):
    layout = InteractiveLayout(selected_border_style="bold yellow")
    layout.split(
        InteractiveLayout(name="header", size=3),
        InteractiveLayout(name="menu", size=3),
        InteractiveLayout(name="main", size=3, selected_border_style="bold red"),
        InteractiveLayout(name="footer", size=3, selected_border_style="bold green"),
    )

    layout["menu"].split_row(
        InteractiveLayout(name="A", ratio=1),
        InteractiveLayout(name="B", ratio=1),
        InteractiveLayout(name="C", ratio=1),
        InteractiveLayout(name="D", ratio=1),
        InteractiveLayout(name="E", ratio=1),
    )

    layout["footer"].split_row(
        InteractiveLayout(name="left", ratio=1),
        InteractiveLayout(name="right", ratio=1),
    )

    for child in layout.children:
        child.update(Panel(Text(child.name, style="yellow")))

    for child in layout["menu"].children:
        child.update(Panel(Text(child.name, style="yellow")))

    layout["footer"]["right"].update(Panel(Text("right", style="yellow")))
    layout["footer"]["left"].update(Panel(Text("left", style="yellow")))

    expected_output = _("""
    [1;33m┏━━━━━━━━━━━━━━━━━━━━━━━┓[0m
    [1;33m┃[0m [33mheader[0m                [1;33m┃[0m
    [1;33m┗━━━━━━━━━━━━━━━━━━━━━━━┛[0m
    ╭───╮╭───╮╭───╮╭───╮╭───╮
    │ [33mA[0m ││ [33mB[0m ││ [33mC[0m ││ [33mD[0m ││ [33mE[0m │
    ╰───╯╰───╯╰───╯╰───╯╰───╯
    ╭───────────────────────╮
    │ [33mmain[0m                  │
    ╰───────────────────────╯
    ╭──────────╮╭───────────╮
    │ [33mleft[0m     ││ [33mright[0m     │
    ╰──────────╯╰───────────╯
    """)
    output = render_to_text(layout, width=25, height=12)
    diff_output(output, expected_output)

    layout.switch_selection()

    expected_output = _("""
    ╭───────────────────────╮
    │ [33mheader[0m                │
    ╰───────────────────────╯
    [1;33m┏━━━┓[0m╭───╮╭───╮╭───╮╭───╮
    [1;33m┃[0m [33mA[0m [1;33m┃[0m│ [33mB[0m ││ [33mC[0m ││ [33mD[0m ││ [33mE[0m │
    [1;33m┗━━━┛[0m╰───╯╰───╯╰───╯╰───╯
    ╭───────────────────────╮
    │ [33mmain[0m                  │
    ╰───────────────────────╯
    ╭──────────╮╭───────────╮
    │ [33mleft[0m     ││ [33mright[0m     │
    ╰──────────╯╰───────────╯
    """)
    output = render_to_text(layout, width=25, height=12)
    diff_output(output, expected_output)

    for __ in range(5):
        layout.switch_selection()

    expected_output = _("""
    ╭───────────────────────╮
    │ [33mheader[0m                │
    ╰───────────────────────╯
    ╭───╮╭───╮╭───╮╭───╮╭───╮
    │ [33mA[0m ││ [33mB[0m ││ [33mC[0m ││ [33mD[0m ││ [33mE[0m │
    ╰───╯╰───╯╰───╯╰───╯╰───╯
    [1;31m┏━━━━━━━━━━━━━━━━━━━━━━━┓[0m
    [1;31m┃[0m [33mmain[0m                  [1;31m┃[0m
    [1;31m┗━━━━━━━━━━━━━━━━━━━━━━━┛[0m
    ╭──────────╮╭───────────╮
    │ [33mleft[0m     ││ [33mright[0m     │
    ╰──────────╯╰───────────╯
    """)
    output = render_to_text(layout, width=25, height=12)
    diff_output(output, expected_output)

    layout.switch_selection()

    expected_output = _("""
    ╭───────────────────────╮
    │ [33mheader[0m                │
    ╰───────────────────────╯
    ╭───╮╭───╮╭───╮╭───╮╭───╮
    │ [33mA[0m ││ [33mB[0m ││ [33mC[0m ││ [33mD[0m ││ [33mE[0m │
    ╰───╯╰───╯╰───╯╰───╯╰───╯
    ╭───────────────────────╮
    │ [33mmain[0m                  │
    ╰───────────────────────╯
    [1;32m┏━━━━━━━━━━┓[0m╭───────────╮
    [1;32m┃[0m [33mleft[0m     [1;32m┃[0m│ [33mright[0m     │
    [1;32m┗━━━━━━━━━━┛[0m╰───────────╯
    """)
    output = render_to_text(layout, width=25, height=12)
    diff_output(output, expected_output)
