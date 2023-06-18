from reactpy import component, html, hooks
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def Item(text, done=False):
  attrs = { "style": { "text-decoration": "line-through" } } if done else {}
  return html.li(attrs, text)

@component
def HelloWorld():
  return html._(
    html.div(
      html.h1("Todo List"),
      html.ul(
        { "style": { "list-style-type": "none" } },
        Item("Learn ReactPy", True),
        Item("Learn FastAPI", True),
        Item("Build something awesome!", False)
      )
    )
  )

app = FastAPI()
configure(app, HelloWorld)
