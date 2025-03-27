import reflex as rx


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.vstack(
                rx.hstack(
                    rx.icon(icon, size=16, stroke_width=1.5),
                    rx.form.label(label),
                    align="center",
                    spacing="2",
                    style={"width": "100%", "margin-bottom": "-1em"},
                ),
                rx.form.control(
                    rx.input(
                        placeholder=placeholder,
                        type=type,
                        default_value=default_value,
                        style={"width": "100%"},
                    ),
                    as_child=True,
                    style={"width": "100%"},
                ),
                style={"width": "100%"},
            ),
            style={"width": "100%"},
        ),
        style={"width": "100%", "margin-bottom": "-1em"},
        align="center",
        name=name,
    )
