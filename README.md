# Rich Interactive
Extends the Rich library with interactive layouts and tables, allowing seamless navigation and interaction via keyboard shortcuts


## Interactive Layouts

You can create interactive layouts that can be easily navigated, and you can switch the selection to any of the children.

```python
console = Console(width=60, height=15)

layout = InteractiveLayout()
layout.split(
    InteractiveLayout(name="header", size=5),
    InteractiveLayout(name="main", size=5),
    InteractiveLayout(name="footer", size=5),
)
layout.traverse()
for child in layout.children:
    child.update(Panel(Text(child.name, style="yellow")))

print("Initial layout:")
print(layout)

layout.switch_selection()

print("After switching selection:")
print(layout)

```

![](./docs/images/interactive_layout.png)
