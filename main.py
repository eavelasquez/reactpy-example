from fastapi import FastAPI
from reactpy import component, event, html, use_state
from reactpy.backend.fastapi import configure, Options
from uuid import uuid4

@component
def Header(on_add_todo):
  return html.header(
    { "class_name": "header" },
    html.h1(
      "todos",
      html.img({ 
        "src": "https://reactpy.dev/docs/_static/reactpy-logo-landscape.svg",
        "alt": "ReactPy Logo",
        "style": { "width": '192px', "height": 'auto' }
      })
    ),
    AddTodo(on_add_todo=on_add_todo)
  )

@component
def Footer(active_todos, completed_todos, filter_selected, on_clear_completed, on_filter_change):
  return html.footer(
    { "class_name": "footer" },
    html.span(
      { "class_name": "todo-count" },
      html.strong(active_todos),
      f" item{'s' if active_todos != 1 else ''} left"
    ),
    TodoFilters(filter_selected=filter_selected, on_filter_change=on_filter_change),
    html.button(
      { 
        "class_name": "clear-completed",
        "on_click": lambda _: on_clear_completed() 
      },
      f"Clear completed ({completed_todos})"
    ) if completed_todos > 0 else ""
  )

@component
def TodoFilters(filter_selected, on_filter_change):
  filters = [
    { "literal": "all", "label": "All" },
    { "literal": "active", "label": "Active" },
    { "literal": "completed", "label": "Completed" }
  ]

  return html.ul(
    { "class_name": "filters" },
    [
      html.li(
        { "key": filter["literal"] },
        html.a(
          {
            "class_name": "selected" if filter_selected == filter["literal"] else "",
            "href": f"#{filter['literal']}",
            "on_click": lambda _: on_filter_change(filter["literal"])
          },
          filter["label"]
        )
      ) for filter in filters
    ]
  )

@component
def AddTodo(on_add_todo):
  title, set_title = use_state("")

  def handle_change(event):
    set_title(event["target"]["value"])

  def handle_add_todo(_):
    if len(title) > 0:
      on_add_todo(title)
      set_title("")

  def handle_key_down(event):
    if event["key"] == "Enter":
      handle_add_todo(event)

  @event(prevent_default=True)
  def handle_submit(event):
    handle_add_todo(event)

  return html.form(
    { "on_submit": handle_submit },
    html.input({
      "autofocus": True,
      "class_name": "new-todo",
      "on_input": handle_change,
      "on_key_down": handle_key_down,
      "placeholder": "What needs to be done?",
      "value": title
    })
  )

@component
def TodoItem(todo, on_remove_todo, on_toggle_todo, on_update_todo):
  new_title, set_new_title = use_state(todo["title"])
  is_editing, set_is_editing = use_state("")
  # input_new_title = use_ref("")

  def handle_title_change(event):
    set_new_title(event["target"]["value"])

  def handle_key_down(event):
    if event["key"] == "Enter":
      set_new_title(new_title.strip())

      if new_title != todo["title"]:
        on_update_todo(id=todo["id"], title=new_title)

      if len(new_title) == 0:
        on_remove_todo()

      set_is_editing("")

    if event["key"] == "Escape":
      set_new_title(todo["title"])
      set_is_editing("")
      
  def handle_blur(_):
    set_new_title(todo["title"])
    set_is_editing("")

  def handle_double_click(_):
    set_is_editing(todo["id"])

  # use_effect(
  #   lambda: input_new_title.current["focus"](),
  #   [is_editing]
  # )

  return html.li(
    {
      "class_name": f"""
        {'completed' if todo['completed'] else ''}
        {'editing' if is_editing == todo['id'] else ''}
      """,
      "on_double_click": handle_double_click,
    },
    html._(
      html.div(
        { "class_name": "view" },
        html.input({
          "checked": todo["completed"],
          "class_name": "toggle",
          "on_change": lambda _: on_toggle_todo(),
          "type": "checkbox"
        }),
        html.label(todo["title"]),
        html.button(
          { "class_name": "destroy", "on_click": lambda _: on_remove_todo() }
        )
      ),

      html.input({
        "class_name": "edit",
        "on_blur": handle_blur,
        "on_change": handle_title_change,
        "on_key_down": handle_key_down,
        # "ref": input_new_title,
        "value": new_title
      })
    )
  )

@component
def TodoList(todos, on_remove_todo, on_toggle_todo, on_update_todo):
  return html.ul(
    { "class_name": "todo-list" },
    [
      TodoItem(
        todo=todo,
        on_remove_todo=lambda id=todo["id"]: on_remove_todo(id),
        on_toggle_todo=lambda id=todo["id"], completed=not todo["completed"]: on_toggle_todo(id, completed),
        on_update_todo=on_update_todo,
        key=todo["id"]
      ) for todo in todos
    ]
  )

@component
def App():
  todos, set_todos = use_state([
    { "id": 1, "title": "Learn ReactPy", "completed": True },
    { "id": 2, "title": "Learn FastAPI", "completed": True },
    { "id": 3, "title": "Build something awesome!", "completed": False }
  ])
  filter_selected, set_filter_selected = use_state("all")

  def handle_filter_change(filter):
    set_filter_selected(filter)

  def add_todo(title):
    new_todo = { "id": uuid4(), "title": title, "completed": False }
    set_todos([*todos, new_todo])

  def remove_todo(id):
    new_todos = [todo for todo in todos if todo["id"] != id]
    set_todos(new_todos)

  def update_todo(id, title):
    new_todos = [
      { **todo, "title": title } if todo["id"] == id else todo
      for todo in todos
    ]
    set_todos(new_todos)

  def toggle_todo(id, completed):
    new_todos = [
      { **todo, "completed": completed } if todo["id"] == id else todo
      for todo in todos
    ]
    set_todos(new_todos)

  def toggle_all():
    new_todos = [
      { **todo, "completed": True } for todo in todos
    ]
    set_todos(new_todos)

  def clear_completed():
    new_todos = [todo for todo in todos if not todo["completed"]]
    set_todos(new_todos)

  active_todos = len([todo for todo in todos if not todo["completed"]])
  completed_todos = len([todo for todo in todos if todo["completed"]])
  filtered_todos = {
    "all": todos,
    "active": [todo for todo in todos if not todo["completed"]],
    "completed": [todo for todo in todos if todo["completed"]]
  }[filter_selected]

  return html._(
    html.div(
      { "class_name": "todoapp" },
      Header(on_add_todo=add_todo),
      html.section(
        { "class_name": "main" },
        html.input({
          "checked": active_todos == 0,
          "class_name": "toggle-all",
          "id": "toggle-all",
          "on_change": lambda _: toggle_all(),
          "type": "checkbox"
        }),
        html.label({ "for": "toggle-all" }, "Mark all as complete"),
        TodoList(
          todos=filtered_todos,
          on_remove_todo=remove_todo,
          on_toggle_todo=toggle_todo,
          on_update_todo=update_todo
        ) if len(todos) > 0 else ""
      ),
      Footer(
        active_todos=active_todos,
        completed_todos=completed_todos,
        filter_selected=filter_selected,
        on_clear_completed=clear_completed,
        on_filter_change=handle_filter_change
      ) if active_todos > 0 or completed_todos > 0 else ""
    )
  )

head = (
  { 'tagName': 'title', 'children': ['Todo App']},
  { 'tagName': 'meta', 'attributes': {'name': 'description', 'content': 'Todo App'}},
  { 'tagName': 'meta', 'attributes': {'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}},
  { 'tagName': 'link', 'attributes': {'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/npm/todomvc-app-css@2.4.2/index.min.css' }},
  { 'tagName': 'link', 'attributes': {'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/npm/todomvc-common@1.0.5/base.min.css' }}
)

app = FastAPI(title="Todo App")
configure(app, App, options=Options(head=head))
