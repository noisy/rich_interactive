import pytest

from rich_interactive.interactive_panel import InteractivePanel as Panel
from tests.utils import adjust_output as _
from tests.utils import diff_output


@pytest.mark.skip(reason="Not implemented yet")
def test_scrollable_table_with_a_scrollbar_on_the_right(render_to_text):
    panel = Panel(
        "Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit, "
        "sed do eiusmod tempor "
        "incididunt ut labore et dolore "
        "magna aliqua. Ut enim ad minim "
        "veniam, quis nostrud "
        "exercitation ullamco laboris "
        "nisi ut aliquip ex ea commodo"
        "consequat.",
        height=9,
        scrollable=True,
    )

    expected_output = _("""
        ╭─────────────────────────────────╮
        │ Lorem ipsum dolor sit amet,    ▲│
        │ consectetur adipiscing elit,   █│
        │ sed do eiusmod tempor          ▒│
        │ incididunt ut labore et dolore ▒│
        │ magna aliqua. Ut enim ad minim ▒│
        │ veniam, quis nostrud           ▒│
        │ exercitation ullamco laboris   ▼│
        ╰─────────────────────────────────╯
    """)

    output = render_to_text(panel, width=35, height=7)
    diff_output(output, expected_output)
