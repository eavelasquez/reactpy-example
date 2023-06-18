from reactpy import component, html
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def Item(text):
  return html.li(text)

@component
def HelloWorld():
  return html._(
    html.div(
      html.h1("Todo List"),
      html.ul(
        Item("Learn React"),
        Item("Learn ReactPy"),
        Item("Build something awesome")
      )
    )
  )

app = FastAPI()
configure(app, HelloWorld)
