import reflex as rx

from ..backend.template import Template
from ..backend.template import TemplateState
from ..backend.applicationsets import ApplicationSetsState
from ..components.form_field import form_field
from ..components.header_cell import header_cell

def _show_templates(tp: Template):
    print("类型判断：")
    print(f"emp 类型: {type(tp)}")
    print(f"Employee 类型: {Template}")
    print(isinstance(tp, Template))
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.row_header_cell(tp.name),
        rx.table.cell(tp.description),
        # rx.table.cell(tp.action),
        rx.table.cell(
            rx.dialog.root(
                rx.dialog.trigger(
                    rx.button(
                        rx.icon("briefcase", size=18),
                        rx.text(tp.action),
                        color_scheme="blue",
                        # on_click=State.create_application(tp),
                        # loading=State.gen_response,
                        style={
                            "margin_right": "1em",
                        },
                    ),
                ),
                _create_application_from_template(tp.name)
            ),
            rx.link(
                rx.button(
                    rx.icon("briefcase", size=18),
                    rx.text("view"),
                    color_scheme="blue",
                    on_click=ApplicationSetsState.list_applicationsets_by_template(tp),
                    # loading=State.gen_response,
                ),
                href=f"/applicationsets/{tp.name}",
            ),
        ),
        style={"_hover": {"bg": rx.color("accent", 2)}},
        align="center",
    )


def _create_application_from_template(tp_name: str) -> rx.Component:
    return rx.dialog.content(
        rx.flex(
            rx.form.root(
                rx.flex(
                    rx.vstack(
                        form_field(
                            "Name",
                            "Application Name",
                            "text",
                            "Name",
                            "user"
                        ),
                        form_field(
                            "Namespace",
                            "Application Namespace",
                            "text",
                            "Namespace",
                            "map-pinned"
                        ),
                        rx.form.field(
                            rx.flex(
                                rx.vstack(
                                    rx.form.control(
                                        rx.input(
                                            type="text",
                                            default_value=tp_name,
                                            value=tp_name,
                                            style={"width": "100%", "display": "none", "margin": "-2em", "padding": "-4em"},
                                        ),
                                        as_child=True,
                                    ),
                                ),
                            ),
                            align="center",
                            name="Template",
                            style={"width": "100%", "display": "none", "margin": "-2em", "padding": "-4em"},
                        ),
                        style={"width": "100%"},
                    ),
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Close",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.form.submit(
                        rx.dialog.close(
                            rx.button(
                                "Submit",
                            ),
                        ),
                        as_child=True,
                    ),
                    padding_top="2em",
                    spacing="3",
                    mt="1",
                    justify="end",
                ),
                on_submit=ApplicationSetsState.create_applicationset,
                reset_on_submit=False,
            ),
            style={"width": "100%"},
            direction="column",
            spacing="4",
        ),
        width="100%",
        max_width="450px",
        justify=["end", "end", "start"],
        border=f"2.5px solid {rx.color('accent', 7)}",
        border_radius="25px",
    )


def main_table():
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("模板名称", "square-user-round"),
                    header_cell("描述", "briefcase"),
                    header_cell("操作", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(TemplateState.templates, _show_templates)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )
