from rich import box
from rich.table import Table

from tests.utils import adjust_output as _
from tests.utils import diff_output


def test_plain_table(render_to_text):
    table = Table(title="Plain Table")
    table.add_column("Column 1", width=12)
    table.add_row("Row 1")

    expected_output = _("""
    [3m  Plain Table   [0m
    ┏━━━━━━━━━━━━━━┓
    ┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━━━━━━━━━━━━┩
    │ Row 1        │
    └──────────────┘
    """)

    output = render_to_text(table)

    diff_output(output, expected_output)


def test_table_with_double_edge_box_and_colors(render_to_text):
    table = Table(
        title="Double Edge Box",
        box=box.DOUBLE_EDGE,
        style="blue",
        header_style="bold green",
        title_style="bold red",
    )
    table.add_column("Column 1", width=12, style="magenta")
    table.add_column("Column 2", width=12, style="bold yellow")
    table.add_row("a", "b")
    table.add_row("c", "d")

    expected_output = _("""
    [1;31m        Double Edge Box        [0m
    [34m╔══════════════╤══════════════╗[0m
    [34m║[0m[1;32m [0m[1;32mColumn 1    [0m[1;32m [0m[34m│[0m[1;32m [0m[1;32mColumn 2    [0m[1;32m [0m[34m║[0m
    [34m╟──────────────┼──────────────╢[0m
    [34m║[0m[35m [0m[35ma           [0m[35m [0m[34m│[0m[1;33m [0m[1;33mb           [0m[1;33m [0m[34m║[0m
    [34m║[0m[35m [0m[35mc           [0m[35m [0m[34m│[0m[1;33m [0m[1;33md           [0m[1;33m [0m[34m║[0m
    [34m╚══════════════╧══════════════╝[0m
    """)

    output = render_to_text(table)

    diff_output(output, expected_output)
