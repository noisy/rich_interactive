import pytest

from rich_interactive.interactive_table import InteractiveTable
from tests.utils import adjust_output as _
from tests.utils import diff_output


def add_columns_and_rows(table, rows=3):
    table.add_column("#")
    table.add_column("Column 1", width=12)
    for i in range(1, rows + 1):
        table.add_row(str(i), f"Row {i}")


def test_default_row_selection(render_to_text):
    table = InteractiveTable(title="Interactive Table")
    add_columns_and_rows(table)

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │[37;100m [0m[37;100m1[0m[37;100m [0m│[37;100m [0m[37;100mRow 1       [0m[37;100m [0m│
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_no_selected_row(render_to_text):
    table = InteractiveTable(title="Interactive Table", selected_row=None)
    add_columns_and_rows(table)

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_selected_row(render_to_text):
    table = InteractiveTable(title="Interactive Table", selected_row=1)
    add_columns_and_rows(table)

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │[37;100m [0m[37;100m2[0m[37;100m [0m│[37;100m [0m[37;100mRow 2       [0m[37;100m [0m│
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_selected_row_moved_down(render_to_text):
    table = InteractiveTable(title="Interactive Table", selected_row=1)
    add_columns_and_rows(table)

    table.move_selection_down()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │ 2 │ Row 2        │
    │[37;100m [0m[37;100m3[0m[37;100m [0m│[37;100m [0m[37;100mRow 3       [0m[37;100m [0m│
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_selected_row_moved_up(render_to_text):
    table = InteractiveTable(title="Interactive Table", selected_row=2)
    add_columns_and_rows(table)

    table.move_selection_up()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │[37;100m [0m[37;100m2[0m[37;100m [0m│[37;100m [0m[37;100mRow 2       [0m[37;100m [0m│
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_last_selected_row_moved_down_does_not_move_selection(
    render_to_text,
):
    table = InteractiveTable(title="Interactive Table", selected_row=2)
    add_columns_and_rows(table)

    table.move_selection_down()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │ 2 │ Row 2        │
    │[37;100m [0m[37;100m3[0m[37;100m [0m│[37;100m [0m[37;100mRow 3       [0m[37;100m [0m│
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_first_selected_row_moved_up_does_not_move_selection(
    render_to_text,
):
    table = InteractiveTable(title="Interactive Table", selected_row=0)
    add_columns_and_rows(table)

    table.move_selection_up()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │[37;100m [0m[37;100m1[0m[37;100m [0m│[37;100m [0m[37;100mRow 1       [0m[37;100m [0m│
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_last_selected_row_moved_down_when_rotate_selection_true_does_move_selection_to_first_row(
    render_to_text,
):
    table = InteractiveTable(title="Interactive Table", selected_row=2, rotate_selection=True)
    add_columns_and_rows(table)

    table.move_selection_down()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │[37;100m [0m[37;100m1[0m[37;100m [0m│[37;100m [0m[37;100mRow 1       [0m[37;100m [0m│
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_first_selected_row_moved_up_when_rotate_selection_true_does_move_selection_to_last_row(
    render_to_text,
):
    table = InteractiveTable(title="Interactive Table", selected_row=0, rotate_selection=True)
    add_columns_and_rows(table)

    table.move_selection_up()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │ 2 │ Row 2        │
    │[37;100m [0m[37;100m3[0m[37;100m [0m│[37;100m [0m[37;100mRow 3       [0m[37;100m [0m│
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)


def test_remove_selection(render_to_text):
    table = InteractiveTable(title="Interactive Table", selected_row=1)
    add_columns_and_rows(table)

    table.remove_selection()

    expected_output = _("""
    [3m Interactive Table  [0m
    ┏━━━┳━━━━━━━━━━━━━━┓
    ┃[1m [0m[1m#[0m[1m [0m┃[1m [0m[1mColumn 1    [0m[1m [0m┃
    ┡━━━╇━━━━━━━━━━━━━━┩
    │ 1 │ Row 1        │
    │ 2 │ Row 2        │
    │ 3 │ Row 3        │
    └───┴──────────────┘
    """)

    output = render_to_text(table)
    diff_output(output, expected_output)
