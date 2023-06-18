from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def Item(text, initial_done=False):
  done, set_done = hooks.use_state(initial_done)
  attrs = { "style": { "text-decoration": "line-through" } } if done else {}

  def toggle_done(_):
    set_done(not done)

  if done:
    return html.li(
      attrs,
      html.span(text),
      html.button({ "on_click": toggle_done }, "Undone!")
    )
  else:
    return html._(
      html.li(
        attrs,
        html.span(text, " ✔"),
        html.button({ "on_click": toggle_done }, "Done!")
      ) 
    )

@component
def DataList(items, filter_by_priority=None, sort_by_priority=False):
  attrs = { "style": { "list-style-type": "none" } }

  if filter_by_priority is not None:
    items = [item for item in items if item["priority"] <= filter_by_priority]

  if sort_by_priority:
    items = sorted(items, key=lambda item: item["priority"])

  list_items_html = [
    Item(item["text"], item["done"]) for item in items
  ]
  return html.ul(attrs, list_items_html)

@component
def TodoList():
  tasks = [
    { "id": 1, "text": "Learn ReactPy", "done": True, "priority": 1 },
    { "id": 2, "text": "Learn FastAPI", "done": True, "priority": 2 },
    { "id": 3, "text": "Build something awesome!", "done": False, "priority": 3 }
  ]

  return html.section(
    html.h1("My Todo List"),
    DataList(tasks, filter_by_priority=3, sort_by_priority=True),
  )

app = FastAPI()
configure(app, TodoList)
