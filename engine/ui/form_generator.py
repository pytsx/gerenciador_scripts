from typing import Literal, List, Callable, Optional, Union
from pydantic import BaseModel
import flet as ft

# Tipos de campo suportados pelo Flet (extensível)
FieldType = Literal[
  "text", "number", "radio", "dropdown", "checkbox", "textarea",
  "password", "email", "date"
]

# Modelos de campos discriminados
class TextField(BaseModel):
  key: str
  label: str
  type: Literal["text", "number", "password", "email", "textarea", "date"]

class RadioField(BaseModel):
  key: str
  label: str
  type: Literal["radio"]
  options: List[str]

class DropdownField(BaseModel):
  key: str
  label: str
  type: Literal["dropdown"]
  options: List[str]

class CheckboxField(BaseModel):
  key: str
  label: str
  type: Literal["checkbox"]

Field = Union[TextField, RadioField, DropdownField, CheckboxField]

class FormPayload(BaseModel):
  title: str
  fields: List[Field]
  on_submit: Optional[Callable[[dict], None]] = None

# Função para gerar o formulário baseado no payload
def form_generator(payload: FormPayload) -> ft.Column:
  state = {}
  controls = []

  for field in payload.fields:
    match field.type:
      case "text" | "password" | "email" | "textarea" | "date":
          control = ft.TextField(
              label=field.label,
              password=field.type == "password",
              multiline=field.type == "textarea",
              keyboard_type=ft.KeyboardType.EMAIL if field.type == "email" else None,
              on_change=lambda e, key=field.key: state.update({key: e.control.value})
          )

      case "number":
          control = ft.TextField(
              label=field.label,
              keyboard_type=ft.KeyboardType.NUMBER,
              on_change=lambda e, key=field.key: state.update({key: int(e.control.value or 0)})
          )

      case "radio":
          control = ft.RadioGroup(
              content=ft.Column([
                  ft.Radio(value=opt, label=opt) for opt in field.options
              ]),
              on_change=lambda e, key=field.key: state.update({key: e.control.value})
          )

      case "dropdown":
          control = ft.Dropdown(
              label=field.label,
              options=[ft.dropdown.Option(opt) for opt in field.options],
              on_change=lambda e, key=field.key: state.update({key: e.control.value})
          )

      case "checkbox":
          control = ft.Checkbox(
              label=field.label,
              on_change=lambda e, key=field.key: state.update({key: e.control.value})
          )

      case _:  # fallback
          control = ft.Text(f"Campo '{field.type}' não suportado")

    controls.append(control)

  # Botão de envio
  def submit_handler(e):
      if payload.on_submit:
          payload.on_submit(state)

  controls.append(ft.ElevatedButton("Enviar", on_click=submit_handler))

  return ft.Column([
      ft.Text(payload.title, size=20, weight="bold"),
      *controls
  ])

