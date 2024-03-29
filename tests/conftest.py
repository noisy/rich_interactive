import io

from pytest import fixture
from rich.console import Console, RenderableType


@fixture
def render_to_text():
    def _render_to_text(
        renderable: RenderableType, width: int = 40, height: int = None
    ):
        output_io = io.StringIO()
        console = Console(file=output_io, width=width, height=height, record=True)

        console.print(renderable)
        console.save_text("tests/.last_render.ans", styles=True, clear=True)

        console.print(renderable)
        return console.export_text(styles=True, clear=True)

    return _render_to_text
