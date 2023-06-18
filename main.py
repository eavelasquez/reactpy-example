from reactpy import component, html
from reactpy.backend.fastapi import configure
from fastapi import FastAPI

@component
def HelloWorld():
  return html._(
    html.div(
      html.h1("Todo List"),
      html.ul(
        html.li("Learn React"),
        html.li("Learn ReactPy"),
        html.li("Build something awesome")
      )
    )
  )

app = FastAPI()
configure(app, HelloWorld)
