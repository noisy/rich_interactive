from rich_interactive.interactive_table import InteractiveTable
from tests.utils import adjust_output as _
from tests.utils import diff_output


def test_interactive_table_default_row_selection(render_to_text):
    table = InteractiveTable(title="Interactive Table")
    table.add_column("#")
    table.add_column("Column 1", width=12)
    table.add_row("1", "Row 1")
    table.add_row("2", "Row 2")
    table.add_row("3", "Row 3")

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │[37;101m [0m[37;101m1[0m[37;101m [0m│[37;101m [0m[37;101mRow 1       [0m[37;101m [0m│
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)

    diff_output(output, expected_output)
