
import reflex as rx


def data_card(title: str, description: str, action: str, action_link: str, action_on_click=None) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title),
            rx.text(description),
            rx.button(
                action,
                color_scheme="blue",
                on_click=action_on_click,
                href=action_link
            ),
            spacing="1em"
        ),
        variant="outlined",
        width="100%",
        padding="1em"
    )