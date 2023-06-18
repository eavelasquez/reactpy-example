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
    return html.li(attrs, html.span(text))
  else:
    return html._(
      html.li(
        attrs,
        html.span(text),
        html.button({ "on_click": toggle_done }, "Done!")
      ) 
    )


@component
def HelloWorld():
  attrs = { "style": { "text-decoration": "line-through" } }

  return html._(
    html.div(
      html.h1("Todo List"),
      html.ul(
        attrs,
        Item("Learn ReactPy", True),
        Item("Learn FastAPI", True),
        Item("Build something awesome!", False)
      )
    )
  )

app = FastAPI()
configure(app, HelloWorld)
