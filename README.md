# Rich Interactive
Extends the Rich library with interactive layouts and tables, allowing seamless navigation and interaction via keyboard shortcuts


## Interactive Layouts

You can create interactive layouts that can be easily navigated, and you can switch the selection to any of the children.

```python
from rich.console import Console
from rich.text import Text

from rich_interactive.interactive_panel import InteractivePanel as Panel
from rich_interactive.interactive_layout import InteractiveLayout as Layout


console = Console(width=60, height=15)

layout = Layout()
layout.split(
    Layout(name="header", size=5),
    Layout(name="main", size=5),
    Layout(name="footer", size=5),
)

for child in layout.children:
    child.update(Panel(Text(child.name, style="yellow")))

print("Initial layout:")
print(layout)

layout.switch_selection()

print("After switching selection:")
print(layout)

```

<!-- ![](./docs/images/interactive_layout.png) -->
![](https://raw.githubusercontent.com/noisy/rich_interactive/main/docs/images/interactive_layout.png)
